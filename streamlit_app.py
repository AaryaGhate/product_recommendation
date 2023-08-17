import streamlit as st
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity


data = pd.read_csv("fashion_products.csv")

# Create interaction matrix and find similarity
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get product recommendations based on product name and category
def get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity, num_recommendations=50):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products by product name and category
    filtered_products = filter_by_product_name_and_category(recommended_products, product_name, category)
    
    return filtered_products

# Function to filter recommended products by product name and category
def filter_by_product_name_and_category(products, product_name, category):
    
    filtered_products=[]
    if product_name in ['T-shirt', 'Jeans']:
         tshirt_recommendations = data[
             (data['Product Name'] == 'T-shirt') &
             (data['Category'] == category)
         ].head(num_recommendations/2)
        
         jeans_recommendations = data[
             (data['Product Name'] == 'Jeans') &
             (data['Category'] == category)  
         ].head(num_recommendations/2)
        
         filtered_products = pd.concat([tshirt_recommendations, jeans_recommendations])
  
    else:
         filtered_products = data[
             (data['Product Name'] == product_name) &
             (data['Category'] == category)&
            
         ]
    
    return filtered_products

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
            random_recommendations = random.sample(list(recommendations['Product ID']), 10)
        else:
            random_recommendations = list(recommendations['Product ID'])
        
        # Display 
        recommended_products_info = data[data['Product ID'].isin(random_recommendations)][['Product ID', 'Product Name', 'Category', 'Brand','Color']]
        st.write("Recommended Products:")
        st.table(recommended_products_info)
        
        
        user_products_info = data[data['User ID'] == user_id][['Product Name', 'Category', 'Brand','Color']].drop_duplicates()
        st.write("Products Related to User ID:")
        st.table(user_products_info)

if __name__ == "__main__":
    main()
