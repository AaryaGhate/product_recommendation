import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv("fashion_products.csv")

# Create user-item interaction matrix
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get product recommendations based on category and size
def get_recommendations(user_id, category, size, bought_product_ids, interaction_matrix, product_similarity, num_recommendations=5):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products by category and size
    filtered_products = filter_by_category_and_size(recommended_products, category, size)
    
    # Exclude already bought products
    filtered_products = [product_id for product_id in filtered_products if product_id not in bought_product_ids]
    
    # Additional recommendation logic based on category
    if category == 'Dress':
        filtered_products = recommend_similar_brand_or_color(filtered_products, 'Dress', bought_product_ids)
    elif category == 'Shoes':
        filtered_products = recommend_similar_brand_or_color(filtered_products, 'Shoes', bought_product_ids)
    elif category == 'Tshirt':
        filtered_products = recommend_similar_brand_or_trend(filtered_products, 'Tshirt', bought_product_ids)
    elif category == 'Jeans':
        filtered_products = recommend_different_color_or_similar_trend(filtered_products, 'Jeans', bought_product_ids)
    elif category == 'Sweater':
        filtered_products = recommend_similar_brand(filtered_products, 'Sweater', bought_product_ids)
    
    return filtered_products

# Function to filter recommended products by category and size
def filter_by_category_and_size(products, category, size):
    return [product_id for product_id in products if data[data['Product ID'] == product_id].iloc[0]['Category'] == category and data[data['Product ID'] == product_id].iloc[0]['Size'] == size]

# Function to recommend products with similar brand or color
def recommend_similar_brand_or_color(products, category, bought_product_ids):
    bought_brands = set(data[data['Product ID'].isin(bought_product_ids)]['Brand'])
    bought_colors = set(data[data['Product ID'].isin(bought_product_ids)]['Color'])
    recommended_products = []
    for product_id in products:
        product_info = data[data['Product ID'] == product_id].iloc[0]
        if product_info['Category'] == category and (product_info['Brand'] in bought_brands or product_info['Color'] in bought_colors):
            recommended_products.append(product_id)
    return recommended_products

# Function to recommend products with similar brand or trend
def recommend_similar_brand_or_trend(products, category, bought_product_ids):
    bought_brands = set(data[data['Product ID'].isin(bought_product_ids)]['Brand'])
    bought_trends = set(data[data['Product ID'].isin(bought_product_ids)]['Trend'])
    recommended_products = []
    for product_id in products:
        product_info = data[data['Product ID'] == product_id].iloc[0]
        if product_info['Category'] == category and (product_info['Brand'] in bought_brands or product_info['Trend'] in bought_trends):
            recommended_products.append(product_id)
    return recommended_products

# Function to recommend products with different color or similar trend
def recommend_different_color_or_similar_trend(products, category, bought_product_ids):
    bought_colors = set(data[data['Product ID'].isin(bought_product_ids)]['Color'])
    bought_trends = set(data[data['Product ID'].isin(bought_product_ids)]['Trend'])
    recommended_products = []
    for product_id in products:
        product_info = data[data['Product ID'] == product_id].iloc[0]
        if product_info['Category'] == category and (product_info['Color'] not in bought_colors or product_info['Trend'] in bought_trends):
            recommended_products.append(product_id)
    return recommended_products

# Function to recommend products with similar brand
def recommend_similar_brand(products, category, bought_product_ids):
    bought_brands = set(data[data['Product ID'].isin(bought_product_ids)]['Brand'])
    recommended_products = []
    for product_id in products:
        product_info = data[data['Product ID'] == product_id].iloc[0]
        if product_info['Category'] == category and product_info['Brand'] in bought_brands:
            recommended_products.append(product_id)
    return recommended_products

# Streamlit app
def main():
    st.title("Fashion Product Recommender")
    st.write("Discover personalized fashion product recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    category = st.selectbox("Select Category", data['Category'].unique())
    size = st.selectbox("Select Size", data['Size'].unique())
    bought_product_ids = st.multiselect("Select Already Bought Products", data['Product ID'].unique())
    
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, category, size, bought_product_ids, interaction_matrix, product_similarity)
        
        # Display recommended product IDs
        st.write("Recommended Product IDs:", recommendations)

if __name__ == "__main__":
    main()
