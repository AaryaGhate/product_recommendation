import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv("fashion_products.csv")

# Create user-item interaction matrix
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get product recommendations based on category and size
def get_recommendations(user_id, category, size, interaction_matrix, product_similarity, num_recommendations=5):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products by category and size
    filtered_products = filter_by_category_and_size(recommended_products, category, size)
    
    return filtered_products

# Function to filter recommended products by category and size
def filter_by_category_and_size(products, category, size):
    return [product_id for product_id in products if data[data['Product ID'] == product_id].iloc[0]['Category'] == category and data[data['Product ID'] == product_id].iloc[0]['Size'] == size]

# Streamlit app
def main():
    st.title("Fashion Product Recommender")
    st.write("Discover personalized fashion product recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    category = st.selectbox("Select Category", data['Category'].unique())
    size = st.selectbox("Select Size", data['Size'].unique())
    
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, category, size, interaction_matrix, product_similarity)
        
        # Display recommended product IDs
        st.write("Recommended Product IDs:", recommendations)

if __name__ == "__main__":
    main()
