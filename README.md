
# ETL App for PDF Data Extraction and Transformation

## Overview

This Streamlit application, named "ETL App," facilitates the extraction, transformation, and export of data from PDF files. It leverages Python libraries such as `pypdf`, `pdfplumber`, `pandas`, and `streamlit` to achieve these tasks efficiently. The app is designed to process PDF files containing structured data, extract relevant information, transform it into a structured format, and export the transformed data to a CSV file.

## Features

- **File Upload**: Users can upload PDF files directly through the Streamlit interface.
  
- **Data Extraction**: The application traverses through each page of the uploaded PDF file to extract specific data points such as observed mass, sample positions, and FLP UV % area.

- **Data Transformation**: Extracted data is organized into a Pandas DataFrame (`df`), where additional transformations such as handling NaN values and merging with supplementary data (e.g., sample positions) are performed.

- **Data Sorting**: The application includes a custom sorting logic to sort the DataFrame (`df_new`) based on a specified column (`Sample Position`) in a structured format.

- **CSV Export**: Once the data is processed and transformed, it is exported into a CSV file (`Updated_plate_2.csv`) for further analysis or integration with other systems.

## Dependencies

Ensure you have the following Python libraries installed:

- `pypdf`
- `pdfplumber`
- `pandas`
- `streamlit`

You can install these dependencies using pip:

```bash
pip install pypdf pdfplumber pandas streamlit
```

## Usage

1. **Clone Repository**:

   ```bash
   git clone <repository_url>
   cd ETL-App
   ```

2. **Install Dependencies**:

   Ensure all dependencies are installed as mentioned above.

3. **Run the Application**:

   Start the Streamlit application locally:

   ```bash
   streamlit run streamlit_app.py
   ```

4. **Upload a PDF File**:

   - Click on "Choose a file" and select a PDF file containing structured data.
   - The application will automatically process the uploaded PDF file.

5. **View Results**:

   - The extracted and transformed data will be displayed in a sorted format on the Streamlit interface.
   - The CSV file (`Updated_plate_2.csv`) will be downloaded automatically, containing the processed data.

## Contributing

Contributions to improve the application's functionality or fix issues are welcome. Fork the repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE).

---
