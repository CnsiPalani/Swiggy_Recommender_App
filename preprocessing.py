# preprocessing.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import pickle

def preprocess_data(input_path, output_path, encoder_path):
    """
    Preprocesses the input CSV data by applying one-hot encoding to specified categorical columns,
    saves the processed data to a new CSV file, and serializes the encoder for future use.

    Args:
        input_path (str): Path to the input CSV file containing raw data.
        output_path (str): Path where the processed CSV file will be saved.
        encoder_path (str): Path where the fitted OneHotEncoder object will be serialized and saved.

    Returns:
        pandas.DataFrame: The processed DataFrame with categorical columns one-hot encoded.

    Notes:
        - The categorical columns 'city', 'main_city', and 'cuisine' are one-hot encoded.
        - The encoder is saved using pickle for reuse in future transformations.
        - Unknown categories during transformation will be ignored.
    """
    df = pd.read_csv(input_path)
    categorical_cols = ['city','main_city', 'cuisine']
    # One-Hot Encoding 
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    # fit: Learns the unique categories in the 'City' column.
    # transform: Converts each category into a one-hot encoded format.
    encoded = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))
    df_encoded = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)
    df_encoded.to_csv(output_path, index=False)
    with open(encoder_path, 'wb') as f:
        pickle.dump(encoder, f)
    return df_encoded

if __name__ == "__main__":
    preprocess_data('cleaned_data.csv', 'encoded_data.csv', 'encoder.pkl')
    print("Data preprocessing completed and saved to encoded_data.csv")