import streamlit as st
import pandas as pd
import pickle
from PIL import Image

st.sidebar.title('Navigation')

# Add menu options
menu_option = st.sidebar.radio('Go to', ['🏠 Home', 'ℹ️ About'])


# Display selected page based on menu option
if menu_option == '🏠 Home':
    st.write('Welcome to the Home page!')

    st.header("Fashion Product Recommendation System")

# Load product list from pickle file
    product_list = pickle.load(open("df.pkl", "rb"))

    # Create DataFrame from product list
    product_df = pd.DataFrame(product_list)

    # Load similarity data
    
    similarity = pickle.load(open("similarity.pkl", "rb"))

    # Display select box with product names
    selected_product = st.selectbox("Select a Product", product_df["product"])

    # Multi-select box for attributes
    selected_attributes = st.multiselect("Select attributes", ["product", 'price', 'Rating', 'category', 'Product_summary'])

    def recommend(product_name):
        product_index = product_df[product_df['product'] == product_name].index[0]
        distances = similarity[product_index]
        product_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_products = []
        for i in product_list:
            recommended_products.append(product_df.iloc[i[0]])
        return recommended_products

    if st.button("Recommend"):
        recommendation = recommend(selected_product)

        # Create a list to store data for each product
        product_data = []
        for product in recommendation:
            data = {}
            if 'product' in selected_attributes:
                data['product'] = product.get('product', 'N/A')   

            if 'category' in selected_attributes:
                data['Category'] = product.get('category', 'N/A')

            if 'Product_summary' in selected_attributes:
                data['Product_summary'] = product.get('Product_summary', 'N/A')

            if 'price' in selected_attributes:
                data['Price'] = product.get('price', 'N/A')

            if 'Rating' in selected_attributes:
                data['Rating'] = product.get('Rating', 'N/A')


            product_data.append(data)

        # Convert the list of dictionaries into a DataFrame
        recommended_df = pd.DataFrame(product_data)

        # Display the DataFrame as a table
        st.table(recommended_df)
    # Add your content for the Home page here
elif menu_option == 'ℹ️ About':
    st.header('Welcome to the About page!')

    st.title('This is a Fashion Product Recommendation System designed to provide personalized product recommendations based on user preferences. It uses a collaborative filtering algorithm to analyze user behavior and similarities between products.')
    st.subheader('The objective of this project is to enhance the shopping experience by helping users discover new fashion products that match their style and preferences.')
    st.subheader('Feel free to explore the system and enjoy personalized recommendations!')
    