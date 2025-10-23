# app.py
import streamlit as st
import pandas as pd
from recommendation import recommend_restaurants

def main():
    st.set_page_config(page_title="Swiggy Restaurant Recommender", layout="wide")
    st.title("🍽️ Swiggy Restaurant Recommendation System")
    st.markdown("""
        <style>
        .main {background-color: #f8f9fa;}
        .stButton>button {background-color: #ff914d; color: white;}
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.header("Filter Your Preferences")
    
    # Use text_input for all fields (no selectbox)
    main_city = st.sidebar.text_input("City")
    city = st.sidebar.text_input("Area Name")
    cuisine = st.sidebar.text_input("Cuisine")
    rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5)
    cost = st.sidebar.number_input("Maximum Cost", min_value=0)

    
    if st.button("Recommend", use_container_width=True):
        with st.spinner("Finding the best restaurants for you..."):
            user_input = {
                'main_city': main_city,
                'city': city,
                'cuisine': cuisine,
                'rating': rating,
                'cost': cost
            }
            results = recommend_restaurants(user_input, 'encoded_data.csv', 'cleaned_data.csv', 'encoder.pkl')
        if results is not None and not results.empty:
            st.success("Here are your recommendations:")
            st.dataframe(results.reset_index(drop=True).style.format({"cost": "₹{:.0f}", "rating": "{:.1f}"}))
        else:
            st.warning("No restaurants found matching your criteria. Please adjust your filters and try again.")

if __name__ == "__main__":
    main()
