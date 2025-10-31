# app.py
import streamlit as st
import pandas as pd
from recommendation import recommend_restaurants

def main():
    st.set_page_config(page_title="Swiggy Restaurant Recommender", layout="wide")
    st.markdown("""
        <style>
        body {
            background: linear-gradient(120deg, #fff7e6 0%, #ffe0b2 40%, #e67e22 100%);
        }
        .app-bg-watermark {
            position: fixed;
            bottom: 10px;
            right: 10px;
            opacity: 0.08;
            z-index: 0;
        }
        .main {background-color: rgba(255,255,255,0.96); border-radius: 12px; padding: 2em;}
        .stButton>button {background-color: #e67e22; color: white; font-weight: bold; border-radius: 8px; transition: background 0.2s, box-shadow 0.2s;}
        .stButton>button:hover {
            background-color: #fb8c00;
            color: #fff;
            box-shadow: 0 2px 8px #e67e22aa;
        }
            input[type="text"], input[type="number"], textarea {
                min-height: 20px !important;
                font-size: 0.85em !important;
                border-radius: 8px !important;
            }
        .custom-title {
            font-size: 2.1em !important;
            font-weight: bold;
            color: #263238;
            margin-bottom: 0.5em;
            text-shadow: 2px 2px 8px #fff0e0;
        }
        .custom-sidebar-title {
            font-size: 1em !important;
            font-weight: bold;
            color: #263238;
            margin-bottom: 0.5em;
            text-shadow: 2px 2px 8px #fff0e0;
        }
    .sidebar .sidebar-content {background-color: #fff7f0; border-radius: 12px;}
    .stDataFrame {background-color: #fff7f0; border-radius: 12px;}
        .badge {
            display: inline-block;
            padding: 0.3em 0.7em;
            border-radius: 8px;
            font-size: 0.95em;
            font-weight: 600;
            margin-right: 0.5em;
        }
        .badge-cuisine {background: #ffe0b2; color: #d35400;}
        .badge-rating {background: #d4edda; color: #155724;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png" width="180" class="app-bg-watermark" />', unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:flex-start;margin-bottom:0.5em;'>
        <img src='https://cdn-icons-png.flaticon.com/512/3075/3075977.png' width='48' style='margin-right:1em;'>
        <div>
            <span style='font-size:2.2em;font-weight:700;color:#1976d2;letter-spacing:1px;'>Swiggy Restaurant Recommendation System</span><br>
            <span style='font-size:1.1em;color:#455a64;font-weight:400;'>Find the best restaurants in your area, tailored to your taste and budget.</span>
        </div>
    </div>
    <hr style='border:1px solid #1976d2;margin-bottom:1.5em;'>
    """, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="custom-sidebar-title">✨ <span style="font-size:1.2em;">Filter Your Preferences</span></div>', unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin:0 0 1em 0;border:1px solid #e67e22;'>", unsafe_allow_html=True)
    main_city = st.sidebar.text_input("🏙️ City", help="Enter the main city (e.g., Bengaluru)")
    city = st.sidebar.text_input("📍 Area Name", help="Enter the area or locality")
    cuisine = st.sidebar.text_input("🍽️ Cuisine", help="E.g., North Indian, Chinese, Italian")
    rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 5.0, 3.5, help="Select minimum rating")
    cost = st.sidebar.number_input("💸 Maximum Cost", min_value=0, help="Set your budget")
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    recommend_btn = st.sidebar.button("🔍 Recommend", use_container_width=True)

    # --- User Query Logging ---
    import os, json
    LOG_PATH = 'user_queries.json'
    def log_user_query(query):
        data = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = []
        data.append(query)
        with open(LOG_PATH, 'w') as f:
            json.dump(data, f)

    if recommend_btn:
        with st.spinner("Finding the best restaurants for you..."):
            user_input = {
                'main_city': main_city,
                'city': city,
                'cuisine': cuisine,
                'rating': rating,
                'cost': cost
            }
            log_user_query(user_input)
            results = recommend_restaurants(user_input, 'encoded_data.csv', 'cleaned_data.csv', 'encoder.pkl')
        if results is not None and not results.empty:
            st.success("Here are your recommendations:")
            results = results.rename(columns={"id":"ID","name":"Name","rating":"Rating","rating_count":"Rating Count","cost": "Cost", "cuisine": "Cuisine", "lic_no": "License No","address": "Address","link": "Link","menu": "Menu", "city": "Area Name", "main_city": "City"})
            display_cols = ['ID', 'Name', 'City', 'Area Name', 'Cost', 'Rating', 'Rating Count', 'Cuisine', 'Address']
            # Collapsible card-style display for each restaurant
            for idx, row in results.reset_index(drop=True)[display_cols].iterrows():
                with st.expander(f"{row['Name']} ({row['City']}, {row['Area Name']})", expanded=True):
                    st.markdown(f"""
                        <div style='background-color:#fff7f0;border-radius:12px;padding:1em;margin-bottom:1em;box-shadow:0 2px 8px #e67e2222;'>
                            <span class='badge badge-cuisine'>{row['Cuisine']}</span>
                            <span class='badge badge-rating'>⭐ {row['Rating']:.1f}</span>
                            <span class='badge' style='background:#e3f2fd;color:#1976d2;'>₹{row['Cost']:.0f}</span>
                            <span class='badge' style='background:#f8bbd0;color:#c2185b;'>{row['Rating Count']} ratings</span><br><br>
                            <b>Address:</b> {row['Address']}<br>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No restaurants found matching your criteria. Please adjust your filters and try again.")

    # --- Analytics Dashboard as Hyperlink ---
    st.sidebar.markdown("<hr style='margin:1em 0;border:1px solid #e67e22;'>", unsafe_allow_html=True)
    dashboard_clicked = st.sidebar.button(
        "📊 Show Analytics Dashboard",
        key="show_dashboard_btn",
        help="Click to view user analytics",
        use_container_width=True,
    )

    if dashboard_clicked:
        st.markdown("""
        <div style='background: #f5f7fa; border-radius: 16px; box-shadow: 0 2px 12px #90caf9aa; padding: 0.2em 0.3em; margin-top: 0.3em; border: 2px solid #1976d2;'>
            <div style='font-size:2em; font-weight:bold; color:#1976d2; margin-bottom:0.3em;'>📊 Analytics Dashboard</div>
        """, unsafe_allow_html=True)
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                try:
                    queries = json.load(f)
                except Exception:
                    queries = []
            if queries:
                df_queries = pd.DataFrame(queries)
                st.markdown(f"<b>Total Queries:</b> <span style='color:#e67e22;font-weight:bold;'>{len(df_queries)}</span>", unsafe_allow_html=True)
                st.markdown("<b>Top Cities:</b>", unsafe_allow_html=True)
                # Get top 5 city counts
                top_cities = df_queries['main_city'].value_counts().head(5)
                top_cities_df = top_cities.reset_index()
                top_cities_df.columns = ['City', 'Count']
                top_cities_df.index = [''] * len(top_cities_df)
                st.dataframe(top_cities_df, use_container_width=True, hide_index=True)
                st.markdown("<b>Top Areas:</b>", unsafe_allow_html=True)
                top_area = df_queries['city'].value_counts().head(5)
                top_area_df = top_area.reset_index()
                top_area_df.columns = ['Area', 'Count']
                top_area_df.index = [''] * len(top_area_df)
                st.dataframe(top_area_df, use_container_width=True, hide_index=True)
                st.markdown("<b>Popular Cuisines:</b>", unsafe_allow_html=True)
                st.dataframe(df_queries['cuisine'].value_counts().head(5), use_container_width=True)
                st.markdown(f"<b>Average Budget:</b> <span style='color:#388e3c;font-weight:bold;'>₹{df_queries['cost'].mean():.0f}</span>", unsafe_allow_html=True)
                csv = df_queries.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Analytics CSV",
                    data=csv,
                    file_name='user_queries_analytics.csv',
                    mime='text/csv',
                )
            else:
                st.info("No queries logged yet.")
        else:
            st.info("No queries logged yet.")
        st.markdown("</div>", unsafe_allow_html=True)
            
if __name__ == "__main__":
    main()
