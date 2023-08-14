import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv("fashion_products.csv")

# Create user-item interaction matrix
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get user's purchased products
def get_user_purchases(user_id):
    user_purchases = data[data['User ID'] == user_id]
    return user_purchases['Product ID'].tolist()

# Function to filter recommended products based on rules
def filter_recommended_products(recommended_products, user_id):
    user_purchases = get_user_purchases(user_id)
    filtered_products = []
    
    for product_id in recommended_products:
        product_row = data[data['Product ID'] == product_id].iloc[0]
        category = product_row['Category']
        size = product_row['Size']
        product_name = product_row['Product Name']
        
        if product_id not in user_purchases and (category, size) in user_purchases:
            if product_name == 'Dress':
                user_dress = user_purchases[(user_purchases['Product Name'] == 'Dress') & ((user_purchases['Brand'] == product_row['Brand']) | (user_purchases['Color'] == product_row['Color']))]
                if not user_dress.empty:
                    filtered_products.append(product_id)

            elif product_name == 'Shoes':
                user_shoes = user_purchases[(user_purchases['Product Name'] == 'Shoes') & ((user_purchases['Brand'] == product_row['Brand']) | (user_purchases['Color'] == product_row['Color']))]
                if not user_shoes.empty:
                    filtered_products.append(product_id)

            elif product_name == 'Tshirt':
                user_tshirt = user_purchases[(user_purchases['Product Name'] == 'Tshirt') & (user_purchases['Brand'] == product_row['Brand'])]
                if not user_tshirt.empty:
                    filtered_products.append(product_id)
                    
            elif product_name == 'Jeans':
                user_jeans = user_purchases[(user_purchases['Product Name'] == 'Jeans') & ((user_purchases['Color'] != product_row['Color']) | (user_purchases['Brand'] == product_row['Brand']))]
                if not user_jeans.empty:
                    filtered_products.append(product_id)
                    
            elif product_name == 'Sweater':
                user_sweater = user_purchases[(user_purchases['Product Name'] == 'Sweater') & ((user_purchases['Color'] == product_row['Color']) | (user_purchases['Brand'] == product_row['Brand']))]
                if not user_sweater.empty:
                    filtered_products.append(product_id)
    
    return filtered_products

# Function to get product recommendations based on user interactions and rules
def get_recommendations(user_id, interaction_matrix, product_similarity, num_recommendations=10):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products based on rules
    filtered_products = filter_recommended_products(recommended_products, user_id)
    
    return filtered_products

# Streamlit app
def main():
    st.title("Personalized Fashion Product Recommender")
    st.write("Discover personalized fashion product recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, interaction_matrix, product_similarity)
        
        # Display recommended product IDs in a tabular format
        recommendations_df = pd.DataFrame(recommendations, columns=["Recommended Product IDs"])
        st.write("Recommended Products:")
        st.dataframe(recommendations_df)

if __name__ == "__main__":
    main()
