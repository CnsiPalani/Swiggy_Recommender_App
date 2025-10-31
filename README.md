
# Swiggy Restaurant Recommendation System

## Overview
This application is a professional, user-friendly restaurant recommendation system built with Python and Streamlit. It helps users discover restaurants tailored to their preferences and provides business owners with market insights through an integrated analytics dashboard.

## Features
- **Personalized Recommendations:**
	- Users filter by City, Area, Cuisine, Minimum Rating, and Maximum Cost.
	- Recommendations are shown in attractive, collapsible cards with badges for cuisine, rating, cost, and rating count.
- **Modern UI:**
	- Professional header with icon, accent color, and subtitle.
	- Sidebar with intuitive icons and section dividers for filters.
	- Responsive design and custom styling for inputs and buttons.
- **Analytics Dashboard:**
	- Accessible via sidebar button.
	- Displays total queries, top cities, top areas, popular cuisines, and average budget in a compact, bordered card.
	- Downloadable CSV report for business analysis.
- **Market Insights & Operational Efficiency:**
	- Logs user queries for trend analysis.
	- Helps businesses optimize offerings based on user preferences.

## How It Works
1. **Data Cleaning:**
	 - Run `data_cleaning.py` to clean and preprocess raw restaurant data.
2. **Preprocessing:**
	 - Run `preprocessing.py` to encode categorical features and save the encoder.
3. **Recommendation Engine:**
	 - Uses cosine similarity to match user preferences with restaurants.
4. **Streamlit App:**
	 - Launch with `streamlit run app.py`.
	 - Use the sidebar to set your preferences and get instant recommendations.
	 - Click the dashboard button to view analytics and download reports.

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies (pandas, scikit-learn, streamlit, etc.)

## Screenshots
_Add screenshots of the UI and analytics dashboard here for better documentation._

## Folder Structure
- `app.py` — Main Streamlit application
- `recommendation.py` — Recommendation logic
- `preprocessing.py` — Data preprocessing and encoding
- `data_cleaning.py` — Data cleaning pipeline
- `cleaned_data.csv` — Cleaned restaurant data
- `encoded_data.csv` — Encoded data for recommendations
- `encoder.pkl` — Saved encoder object
- `user_queries.json` — Logged user queries for analytics

## Usage
```bash
streamlit run app.py
```

## License
MIT
