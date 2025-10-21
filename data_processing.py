import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pickle
import streamlit as st

# Load dataset
df = pd.read_csv('swiggy.csv')  # Use relative path for portability


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

# Remove duplicates and handle missing values
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df.to_csv("cleaned_data.csv", index=False)
st.write("Data processing complete. Encoded data saved to 'encoded_data.csv'.")

# One-Hot Encoding for categorical features (exclude 'name' to avoid high cardinality)
# Only encode 'city' and 'cuisine' to avoid memory issues
categorical_cols = ['city', 'cuisine']
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded = encoder.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))
st.write("One-Hot Encoding complete. Only 'city' and 'cuisine' encoded.")

# Combine with numerical features
numerical_cols = ['rating', 'rating_count', 'cost']
final_df = pd.concat([encoded_df, df[numerical_cols].reset_index(drop=True)], axis=1)
final_df.to_csv("encoded_data.csv", index=False)
st.write("numerical_cols combined. Encoded data saved to 'encoded_data.csv'.")
# Save encoder for later use
with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)


# st.write("Data processing complete. encoder.pkl")
