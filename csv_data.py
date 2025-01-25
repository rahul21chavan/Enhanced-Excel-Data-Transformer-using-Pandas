import streamlit as st
import pandas as pd
import google.generativeai as genai
import io
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def transform_data_pandas(data, sort_column=None, fill_missing=False):
    """Transforms data using pandas: sorts data, fills missing column names, and extracts head(10) and tail(5)."""
    # Ensure column names are valid
    data.columns = [f"Column_{i + 1}" if not col else col for i, col in enumerate(data.columns)]

    # Sort values if sort_column is provided
    if sort_column and sort_column in data.columns:
        if pd.api.types.is_numeric_dtype(data[sort_column]):
            data = data.sort_values(by=sort_column)
        else:
            data = data.sort_values(by=sort_column, key=lambda col: col.astype(str))

    # Fill missing values with 'Unknown' if fill_missing is True
    if fill_missing:
        data = data.fillna('Unknown')

    # Extract head(10) and tail(5)
    transformed_data = pd.concat([data.head(10), data.tail(5)])

    return transformed_data


# Streamlit UI
st.title("Enhanced Excel Data Transformer using Pandas")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Load data
        df = pd.read_excel(uploaded_file)
        st.write("### Uploaded Data:")
        st.dataframe(df)

        # Display metadata
        st.write(f"**Shape of Data:** {df.shape[0]} rows x {df.shape[1]} columns")
        st.write(f"**Column Types:**")
        st.write(df.dtypes)

        # Select transformation options
        sort_column = st.selectbox("Sort by which column?", options=[None] + list(df.columns))
        fill_missing = st.checkbox("Fill missing values with 'Unknown'", value=False)

        # Transform data
        with st.spinner("Processing data using Pandas..."):
            transformed_df = transform_data_pandas(df, sort_column, fill_missing)

        st.write("### Transformed Data (Head 10 + Tail 5):")
        st.dataframe(transformed_df)

        # Download transformed data
        csv = transformed_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Transformed Data", csv, "transformed_data.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
