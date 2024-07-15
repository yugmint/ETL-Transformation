import pandas as pd
import streamlit as st
import pypdf as pdf
import pdfplumber as plumber
import io
import re
import os

st.title("ETL App")
st.write("Import your files")
files = st.file_uploader("Choose PDF Files", accept_multiple_files=True)

if files:
    for file in files:
        st.write(f"Processing file: {file.name}")

        # Open the PDF using pypdf
        data = pdf.PdfReader(file)

        # Extracting data from PDF pages
        Obs_mass = []
        sam_pos = []
        flp = []
        obs_temp = []
        for i in range(len(data.pages)):
            page_no = data.pages[i]
            txt = page_no.extract_text().split()
            for j, x in enumerate(txt):
                if x == "(Da)":
                    ind_1 = j + 10
                    ind_temp = ind_1 + 5
                    if len(txt[ind_temp]) == 9:
                        Obs_mass.append([txt[ind_1], txt[ind_temp]])
                    else:
                        Obs_mass.append(txt[ind_1])
                    ind_2 = j - 8
                    sam_pos.append(txt[ind_2])
                    ind_3 = j + 12
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
        data_1 = pdfplumber.open(io.BytesIO(file.read()))

        position = []
        for i in range(len(data_1.pages)):
            try:
                table = data_1.pages[i].extract_table()
                if table[0][2] == 'Sample type':
                    position.append(table[1][-2])
                else:
                    pass
            except IndexError:
                continue
            except TypeError:
                continue

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
        
        # Generate CSV file name based on uploaded PDF file name
        pdf_filename = file.name
        csv_filename = f"Updated_{pdf_filename}.csv"
        
        # Save CSV file to the same path as PDF file
        save_path = os.path.dirname(file.name)
        csv_path = os.path.join(save_path, csv_filename)

        # Exporting to CSV
        csv_data = sorted_df.to_csv(index=False)
        with open(csv_path, 'w') as f:
            f.write(csv_data)

        st.write(f"Exported the file to {csv_path}")
