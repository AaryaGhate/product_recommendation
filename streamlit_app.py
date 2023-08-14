# Function to get product recommendations based on product name and category
def get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity, num_recommendations=50):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    if product_name == "tshirt":
        # Filter recommended products by product name and category
        tshirt_recommended_products = filter_by_product_name_and_category(recommended_products, "tshirt", category)
        jeans_recommended_products = filter_by_product_name_and_category(recommended_products, "jeans", category)
        
        recommended_products = []
        tshirt_count = 0
        
        for product in tshirt_recommended_products:
            if tshirt_count < 5:
                recommended_products.append(product)
                tshirt_count += 1
            else:
                break
        
        for product in jeans_recommended_products:
            recommended_products.append(product)
            if len(recommended_products) >= 10:
                break
        
        return recommended_products
        
    elif product_name == "jeans":
        # Filter recommended products by product name and category
        jeans_recommended_products = filter_by_product_name_and_category(recommended_products, "jeans", category)
        tshirt_recommended_products = filter_by_product_name_and_category(recommended_products, "tshirt", category)
        
        recommended_products = []
        jeans_count = 0
        
        for product in jeans_recommended_products:
            if jeans_count < 5:
                recommended_products.append(product)
                jeans_count += 1
            else:
                break
        
        for product in tshirt_recommended_products:
            recommended_products.append(product)
            if len(recommended_products) >= 10:
                break
        
        return recommended_products
        
    else:
        # Filter recommended products by product name and category
        filtered_products = filter_by_product_name_and_category(recommended_products, product_name, category)
        
        return filtered_products
