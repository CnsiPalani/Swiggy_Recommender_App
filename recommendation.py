# recommendation.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def recommend_restaurants(user_input, encoded_path, cleaned_path, encoder_path, top_n=5):
    # Ensure numeric columns are loaded as numbers
    encoded_df = pd.read_csv(encoded_path, low_memory=False)
    cleaned_df = pd.read_csv(cleaned_path)
    # Filter both encoded and cleaned data by city and main_city
    if 'city' in user_input and user_input['city']:
        city_mask = cleaned_df['city'].str.lower() == user_input['city'].strip().lower()
        cleaned_df = cleaned_df[city_mask]
        encoded_df = encoded_df[city_mask]
    if 'main_city' in user_input and user_input['main_city']:
        main_city_mask = cleaned_df['main_city'].str.lower() == user_input['main_city'].strip().lower()
        cleaned_df = cleaned_df[main_city_mask]
        encoded_df = encoded_df[main_city_mask]
    for col in ['rating', 'rating_count', 'cost']:
        if col in encoded_df.columns:
            encoded_df[col] = pd.to_numeric(encoded_df[col], errors='coerce')

    # Filter by maximum cost if provided BEFORE similarity
    if 'cost' in user_input and user_input['cost']:
        cost_mask = encoded_df['cost'] <= float(user_input['cost'])
        encoded_df = encoded_df[cost_mask]
        cleaned_df = cleaned_df[cost_mask]
    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)
    categorical_cols = ['city', 'main_city', 'cuisine']
    user_input_df = pd.DataFrame([{k: user_input.get(k, None) for k in categorical_cols}])
    user_vec = encoder.transform(user_input_df)
    user_vec_df = pd.DataFrame(user_vec, columns=encoder.get_feature_names_out(categorical_cols))
    for col in ['rating', 'rating_count', 'cost']:
        if col in user_input:
            user_vec_df[col] = user_input[col]
        else:
            user_vec_df[col] = encoded_df[col].mean() if not encoded_df.empty else 0
    user_vec_df = user_vec_df.reindex(columns=encoded_df.columns, fill_value=0)
    # If no data after filtering, return empty DataFrame
    if encoded_df.empty:
        return cleaned_df.head(0)
    encoded_numeric = encoded_df.select_dtypes(include=['number'])
    user_vec_numeric = user_vec_df[encoded_numeric.columns]
    similarities = cosine_similarity(encoded_numeric, user_vec_numeric)
    top_indices = similarities.flatten().argsort()[-top_n:][::-1]
    results = cleaned_df.iloc[top_indices]
    return results
