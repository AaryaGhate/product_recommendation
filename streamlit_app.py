import streamlit as st
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv("fashion_products.csv")

# Create user-item interaction matrix
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to filter recommended products by product name and category
def filter_by_product_name_and_category(products, product_name, category):
    return products[(products['Product Name'] == product_name) & (products['Category'] == category)]


# Function to get product recommendations based on product name and category
def get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity, num_recommendations=50):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    if product_name == "tshirt":
        tshirt_recommended_products = filter_by_product_name_and_category(data, "tshirt", category)
        jeans_recommended_products = filter_by_product_name_and_category(data, "jeans", category)
        
        recommended_products = []
        tshirt_count = 0
        
        for product in tshirt_recommended_products['Product ID']:
            if tshirt_count < 5:
                recommended_products.append(product)
                tshirt_count += 1
            else:
                break
        
        for product in jeans_recommended_products['Product ID']:
            recommended_products.append(product)
            if len(recommended_products) >= 10:
                break
        
        return recommended_products
        
    elif product_name == "jeans":
        jeans_recommended_products = filter_by_product_name_and_category(data, "jeans", category)
        tshirt_recommended_products = filter_by_product_name_and_category(data, "tshirt", category)
        
        recommended_products = []
        jeans_count = 0
        
        for product in jeans_recommended_products['Product ID']:
            if jeans_count < 5:
                recommended_products.append(product)
                jeans_count += 1
            else:
                break
        
        for product in tshirt_recommended_products['Product ID']:
            recommended_products.append(product)
            if len(recommended_products) >= 10:
                break
        
        return recommended_products
        
    else:
        filtered_products = filter_by_product_name_and_category(data, product_name, category)
        
        # Sort the products based on matching brand with the user's selected brand
        user_brand = data[(data['User ID'] == user_id) & (data['Category'] == category)]['Brand'].iloc[0]
        matching_brand_mask = filtered_products['Brand'] == user_brand
        sorted_products = filtered_products[matching_brand_mask].append(filtered_products[~matching_brand_mask])
        
        return sorted_products['Product ID']




# Streamlit app
def main():
    st.title("Fashion Product Recommender")
    st.write("Discover personalized fashion product recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    product_name = st.selectbox("Select Product Name", data['Product Name'].unique())
    category = st.selectbox("Select Category", data['Category'].unique())
    
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity)
        
        if len(recommendations) > 10:
            random_recommendations = random.sample(recommendations, 10)
        else:
            random_recommendations = recommendations
        
        recommended_products_info = data[data['Product ID'].isin(random_recommendations)][['Product ID', 'Product Name', 'Category', 'Brand']]
        st.write("Recommended Products:")
        st.table(recommended_products_info)

if __name__ == "__main__":
    main()
