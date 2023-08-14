import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


data = pd.read_csv("fashion_products.csv")


interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

#Function to get product recommendations
def get_recommendations(user_id, interaction_matrix, product_similarity, num_recommendations=5):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    return recommended_products

# Streamlit app
def main():

    bg_color = "#000000"  # Black background
    text_color = "#FFFFFF"  # White text color

    # Apply the styling to the whole Streamlit app
    st.markdown(
        f"""
        <style>
            body {{
            background-color: {bg_color};
            color: {text_color};
    }}
        </style>
    """,
    unsafe_allow_html=True,
    )
    st.title("Fashion Product Recommender")
    st.write("Discover personalized fashion product recommendations.")
    
    # User input for selecting a user ID
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    
    # Get recommendations when user clicks a button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, interaction_matrix, product_similarity)
        
        # Display recommended product IDs
        st.write("Recommended Product IDs:", recommendations)

if __name__ == "__main__":
    main()
