import streamlit as st
import requests
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Set page config at the very top
st.set_page_config(page_title="🛒 E-Commerce ChatBot", layout="wide")

# Load environment variables
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY_COM")
api_version = os.getenv("AZURE_OPENAI_API_VERSION_PRE", "2025-03-01-preview")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_URL")
deployment_model = os.getenv("AZURE_DEPLOYMENT_MODEL")

# Azure Client Setup
client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=endpoint)
llm = AzureChatOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version,
    deployment_name=deployment_model,
    temperature=0
)

def ecommerce_chatbot():
    st.title("🛍️ E-Commerce ChatBot")

    if "products" not in st.session_state:
        try:
            prod_response = requests.get("https://fakestoreapi.com/products")
            cart_response = requests.get("https://fakestoreapi.com/carts")
            if prod_response.status_code == 200 and cart_response.status_code == 200:
                st.session_state.products = prod_response.json()
                st.session_state.carts = cart_response.json()
            else:
                st.error("Failed to fetch data from the API.")
                st.session_state.products = []
                st.session_state.carts = []
        except Exception as e:
            st.error(f"Error fetching API data: {e}")
            st.session_state.products = []
            st.session_state.carts = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.chat_input("Ask me about products or carts!")

    if user_query:
        response = "I'm not sure how to answer that."

        try:
            products = st.session_state.products
            carts = st.session_state.carts
            product_titles = [p['title'] for p in products]

            # Handle product related questions
            if "what" in user_query.lower() and "product" in user_query.lower():
                response = "Here are the available products:\n\n" + "\n".join(f"- {title}" for title in product_titles[:10])

            elif "cart" in user_query.lower():
                found = False
                # Try to find a cart id in the query
                for word in user_query.split():
                    if word.isdigit():
                        cart_id = int(word)
                        cart_data = next((cart for cart in carts if cart["id"] == cart_id), None)
                        if cart_data:
                            products_in_cart = cart_data.get("products", [])
                            cart_items_list = []
                            for item in products_in_cart:
                                product_id = item.get("productId")
                                quantity = item.get("quantity")
                                product_info = next((p for p in products if p["id"] == product_id), {})
                                cart_items_list.append(f"{product_info.get('title', 'Unknown Product')} (x{quantity})")
                            response = f"**Cart {cart_id} contains:**\n\n" + "\n".join(f"- {item}" for item in cart_items_list[:10])
                            found = True
                        break
                if not found:
                    response = "Sorry, I couldn't find that cart. Please check the cart ID."

            else:
                # Product detail search
                found = False
                for product in products:
                    if (product["title"].lower() in user_query.lower()) or (product["description"].lower() in user_query.lower()):
                        response = f"""
### {product['title']}
**Rating:** {product['rating']} 
**Price:** ${product['price']}  
**Category:** {product['category']}  
**Description:** {product['description']}  
"""
                        found = True
                        break

                if not found:
                    # Use Azure OpenAI fallback
                    system_message = SystemMessage(content="You are a helpful assistant for an e-commerce store. You have products and carts available. Answer based on them.")
                    human_message = HumanMessage(content=f"Products: {product_titles}\nCarts: {[c['id'] for c in carts]}\n\nUser question: {user_query}")
                    ai_response = llm([system_message, human_message])
                    response = ai_response.content.strip()

        except Exception as e:
            response = f"Error: {e}"

        st.session_state.chat_history.append((user_query, response))

    # Display chat history
    for user, bot in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(user)
        with st.chat_message("assistant"):
            st.markdown(bot, unsafe_allow_html=True)

# Run the app
ecommerce_chatbot()
