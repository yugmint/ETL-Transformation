import pandas as pd
import streamlit as st
import pypdf as pdf
import pdfplumber
import io
import re

st.title("ETL App")
st.write("Import your file")
file = st.file_uploader("Choose a PDF File", accept_multiple_files=True)
if file is not None:
    # Open the PDF using pypdf
    
    data = pdf.PdfReader(file)

    # Extracting data from PDF pages
    Obs_mass=[]
    sam_pos=[]
    flp=[]
    obs_temp=[]
    for i in range(len(data.pages)):
        page_no=data.pages[i]
        txt=page_no.extract_text().split()
        for j, x in enumerate(txt):
            if x == "(Da)":
                ind_1=j+10
                ind_temp=ind_1+5
                if len(txt[ind_temp]) == 9:
                    Obs_mass.append([txt[ind_1],txt[ind_temp]])
                else:
                    Obs_mass.append(txt[ind_1])
                ind_2= j-8
                sam_pos.append(txt[ind_2])
                ind_3= j+12
                flp.append(txt[ind_3])
            else:
                pass

    # Creating DataFrame
    df = pd.DataFrame({
        "Sample Position": sam_pos,
        "Observed Mass (Da)": Obs_mass,
        "FLP UV % Area": flp
    })

    # Finding NaN values
    data_1= data
### pdf_file = io.BytesIO(data.read())
    pdf_file = io.BytesIO(file.read())
    data_1 = pdfplumber.open(pdf_file)

    position=[]
    for i in range(len(data_1.pages)):
        try:
            table=data_1.pages[i].extract_table()
            if table[0][2] == 'Sample type':
                position.append(table[1][-2])
            else:
                pass
        except IndexError:
            continue
        except TypeError:
            continue
            # Handle other exceptions
            #print(f"An error occurred for page {i}: {e}")

    # Creating DataFrame for sample positions
    sample_df = pd.DataFrame({"Sample Position": position})
    df["Sample Position"] = df["Sample Position"].str[:-1]

    # Merging both DataFrames
    df_new = pd.merge(df, sample_df, on="Sample Position", how='outer')

    # Sorting DataFrame
    def custom_sort_logic(value):
        match = re.match(r'(\d+)\s*:\s*(\w+)\s*,\s*(\d+)', value)
        if match:
            section1 = int(match.group(1))
            section2 = match.group(2)
            section3 = int(match.group(3))
            return (section1, section3, section2)
        else:
            return (float('inf'), '', float('inf'))

    def sort_dataframe(df, column_name):
        df_sorted = df.sort_values(by=column_name, key=lambda x: x.apply(custom_sort_logic))
        
        return df_sorted
    sorted_df = sort_dataframe(df_new, 'Sample Position')


    # Generate CSV file name based on uploaded PDF file name
    pdf_filename = file.name
    csv_filename = f"Updated_{pdf_filename}.csv"

    # Exporting to CSV
    st.write(f"Exporting the file into {csv_filename}")
    csv_data = sorted_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=csv_filename,
        mime="text/csv"
    )
