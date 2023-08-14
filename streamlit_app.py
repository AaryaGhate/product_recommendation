import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv("fashion_products.csv")

# Create user-item interaction matrix
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get user's preferred category and size
def get_user_preferences(user_id):
    user_purchases = data[data['User ID'] == user_id]
    preferred_category = user_purchases['Category'].mode().values[0]
    preferred_size = user_purchases['Size'].mode().values[0]
    return preferred_category, preferred_size

# Function to filter recommended products by user preferences and product name
def filter_by_user_preferences(products, preferred_category, preferred_size, user_id):
    filtered_products = []
    
    for product_id in products:
        product_row = data[data['Product ID'] == product_id].iloc[0]
        product_category = product_row['Category']
        product_name = product_row['Product Name']
        
        if product_name == 'Dress':
            if product_category == preferred_category or product_row['Brand'] == data[(data['User ID'] == user_id) & (data['Product Name'] == 'Dress')]['Brand'].values[0] or product_row['Color'] == data[(data['User ID'] == user_id) & (data['Product Name'] == 'Dress')]['Color'].values[0]:
                filtered_products.append(product_id)
        
        elif product_name == 'Shoes':
            if product_category == preferred_category or product_row['Brand'] == data[(data['User ID'] == user_id) & (data['Product Name'] == 'Shoes')]['Brand'].values[0] or product_row['Color'] == data[(data['User ID'] == user_id) & (data['Product Name'] == 'Shoes')]['Color'].values[0]:
                filtered_products.append(product_id)
        
        elif product_name == 'Tshirt':
            if product_category == preferred_category or product_row['Brand'] == data[(data['User ID'] == user_id) & (data['Product Name'] == 'Tshirt')]['Brand'].values[0]:
                filtered_products.append(product_id)
        
        elif product_name == 'Jeans':
            if product_category == preferred_category or product_row['Color'] != data[(data['User ID'] == user_id) & (data['Product Name'] == 'Jeans')]['Color'].values[0]:
                filtered_products.append(product_id)
        
        elif product_name == 'Sweater':
            if product_row['Brand'] == data[(data['User ID'] == user_id) & (data['Product Name'] == 'Sweater')]['Brand'].values[0]:
                filtered_products.append(product_id)
    
    return filtered_products

# Function to get product recommendations based on user preferences
def get_recommendations(user_id, interaction_matrix, product_similarity, num_recommendations=5):
    preferred_category, preferred_size = get_user_preferences(user_id)
    
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products by user preferences and product name
    filtered_products = filter_by_user_preferences(recommended_products, preferred_category, preferred_size, user_id)
    
    return filtered_products

# Streamlit app
def main():
    st.title("Fashion Product Recommender")
    st.write("Discover personalized fashion product recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, interaction_matrix, product_similarity)
        
        # Display recommended product IDs
        st.write("Recommended Product IDs:", recommendations)

if __name__ == "__main__":
    main()
