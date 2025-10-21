import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pickle


# Load cleaned and encoded data
df = pd.read_csv("cleaned_data.csv")
encoded_df = pd.read_csv("encoded_data.csv")
with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# Streamlit UI
st.title("Swiggy Restaurant Recommendation System")

city = st.selectbox("Select City", df['city'].unique())
cuisine = st.selectbox("Select Cuisine", df['cuisine'].unique())
rating = st.slider("Minimum Rating", 0.0, 5.0, 3.5)
cost = st.slider("Maximum Cost", 100, 2000, 500)

# Encode user input
user_input = pd.DataFrame([[city, cuisine, 'dummy']], columns=['city', 'cuisine', 'name'])
user_encoded = encoder.transform(user_input)
user_vector = np.append(user_encoded[0], [rating, 0, cost])  # rating_count set to 0
# Compute similarity
similarity = cosine_similarity([user_vector], encoded_df.values)
top_indices = similarity[0].argsort()[-5:][::-1]

# Display recommendations
st.subheader("Recommended Restaurants")
recommendations = df.iloc[top_indices][['name', 'city', 'rating', 'cost', 'cuisine']]
st.dataframe(recommendations)