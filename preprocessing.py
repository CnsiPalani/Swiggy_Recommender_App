# preprocessing.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import pickle

def preprocess_data(input_path, output_path, encoder_path):
    df = pd.read_csv(input_path)
    categorical_cols = ['city','main_city', 'cuisine']
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
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