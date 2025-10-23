# data_cleaning.py
import pandas as pd
import numpy as np
import re
def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # Missing Value Handling:
    # Replaced placeholders like '--' and 'Too Few Ratings' with NaN.
    df.replace({'--': np.nan, 'Too Few Ratings': np.nan}, inplace=True)
    # Replaced 'license' in the lic_no column with NaN.
    df['lic_no'] = df['lic_no'].replace('license', np.nan)

    # Data Type Conversion:
    # Converted rating to float.
    df['rating'] = df['rating'].astype(float)
    # Extracted numeric values from rating_count and converted to float.
    df['rating_count'] = df['rating_count'].str.extract(r'(\d+)').astype(float)

    # Cleaned cost column by removing currency symbols and converting to float.
    df['cost'] = df['cost'].replace({'₹': '', ',': ''}, regex=True).astype(float)
    df = df.drop_duplicates()
    df = df.dropna()

    # Handle city column: split comma, ampersand, or underscore-separated values, assign first to 'city', second (if present) to 'main_city'
    # Some row values in city column have multiple cities separated by ',', '&', or '_'. If the split size is greater than 1, assign first and second to 'city' and third to 'main_city'. If only one city, assign it to 'city' and NaN to 'main_city'.
    
    # Split city column on ',', '&', or '_', assign first to 'city', second to 'main_city'.

    
    df[['city', 'main_city']] = df['city'].apply(process_city)

    # Save cleaned data
    df.to_csv(output_path, index=False)
    return df
def process_city(city):
    # Split city column on ',', '&', or '_', assign first to 'city', second to 'main_city'.
    
    
    parts = [p.strip() for p in re.split(r'\s*[,&_]\s*', str(city)) if p.strip()]
    
    if len(parts) == 1:
        return pd.Series([parts[0], None])
    elif len(parts) == 2:
        return pd.Series([parts[0], parts[1]])
    else:
        return pd.Series([f"{parts[0]}, {parts[1]}", parts[2]])


if __name__ == "__main__":
    clean_data('swiggy.csv', 'cleaned_data.csv')
    print("Data cleaning completed and saved to cleaned_data.csv")
