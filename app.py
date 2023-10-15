# load key libraries and packages
import streamlit as st
import pickle
import joblib
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor

# Define key functions
# Function to load toolkit
def load_toolkit(relative_path):
    with open(relative_path, "rb") as file:
        loaded_tk = joblib.load(file)
    return loaded_tk

# load the toolkit
loaded_toolkit = load_toolkit(r"C:\Users\user\Desktop\Streamlit\Streamlit_Project\src\Streamlit_toolkit")

# instantiate the items in the toolkit
encoder= loaded_toolkit["encoder"]

# import the model
model = DecisionTreeRegressor()
model = joblib.load("src/model.pkl")

# Define a function to load data
@st.cache_resource()
def load_data(relative_path):
    data = pd.read_csv(r"C:\Users\user\Desktop\Streamlit\Streamlit_Project\Data\test.csv")
    return data

# load the dataset
rel_path = r"C:\Users\user\Desktop\Streamlit\Streamlit_Project\Data\test.csv"
loaded_df = load_data(rel_path)

# set app title
st.title("Store Sales Prediction")

# define app sections
header = st.container()
dataset = st.container()
predictions = st.container()

# Set up  the 'header' section
with header:
    header.write("This app predicts the total sales of items sold at different stores")
    header.write("---")

# Set up the 'dataset' section
with dataset:
    if dataset.checkbox("Preview the Dataset"):
        dataset.write(loaded_df)
        dataset.markdown("Kindly check the sidebar for information")
        dataset.write("---")

# set up the Streamlit 'sidebar' for navigation
st.sidebar.header('Navigation')
menu= ['About the App', 'Data Dictionary']
choice= st.sidebar.selectbox("Select an option", menu)

# Define content for each menu option
if choice == 'About the App':
    st.sidebar.subheader('About the App')
    st.sidebar.write("Welcome to the Sales Prediction App, a powerful tool designed to help businesses forecast and optimize their sales performance. This user-friendly application leverages machine learning to provide valuable insights into your future sales trends, allowing you to make informed decisions and drive revenue growth..")

elif choice == 'Data Dictionary':
    st.sidebar.subheader('Data Dictionary')
    st.sidebar.write("Here is the data dictionary for the dataset used in this app:")
    st.sidebar.write("store_nbr: The store which the product is sold")
    st.sidebar.write("product: The product being sold")
    st.sidebar.write("onpromotion: Total number of items in a product family that were being promoted at a store at a given date")
    st.sidebar.write("oil_prices: The current price of oil")
    st.sidebar.write("city: The city which the store is located")
    st.sidebar.write("state: The state which the store is located")
    st.sidebar.write("stores_type: The type of store the product is being sold")
    st.sidebar.write("cluster: The cluster of the store the product is being sold")
    st.sidebar.write("Year: The year you want to predict")
    st.sidebar.write("Month: The month you want to predict")
    st.sidebar.write("Day: The day you want to predict")

# define the form for user inputs
form = st.form(key= "Information", clear_on_submit=True)

# Create key lists
expected_inputs = ["store_nbr","product","onpromotion","oil_prices","city","state","stores_type","cluster","Year","Month","Day"]
cat_columns =["product","city","state","stores_type"]
remaining_columns=["store_nbr","onpromotion","oil_prices","cluster","Year","Month","Day"]

# Set up the 'predictions' section
with predictions:
    predictions.subheader("Inputs")
    predictions.write("This section will take all your inputs")

    # Define columns for user input fields
    col1, col2 = predictions.columns(2)

    # Set up the form
    with form:
        # set up col1
        col1.write("Inputs Part 1:")
        store_nbr = col1.number_input("Which store is the product sold?", min_value=1, max_value=54)
        product = col1.selectbox("What is the product sold?", options= [
        "MEATS",
        "PREPARED FOODS",
        "HOME AND KITCHEN I",
        "BOOKS",
        "SEAFOOD",
        "SCHOOL AND OFFICE SUPPLIES",
        "HOME AND KITCHEN II",
        "HOME CARE",
        "CLEANING",
        "PLAYERS AND ELECTRONICS",
        "HARDWARE",
        "HOME APPLIANCES",
        "PRODUCE",
        "BEVERAGES",
        "PET SUPPLIES",
        "BREAD/BAKERY",
        "AUTOMOTIVE",
        "GROCERY II",
        "PERSONAL CARE",
        "DAIRY",
        "LINGERIE",
        "FROZEN FOODS",
        "LAWN AND GARDEN",
        "DELI",
        "MAGAZINES",
        "EGGS",
        "BEAUTY",
        "LADIESWEAR",
        "LIQUOR,WINE,BEER",
        "GROCERY I",
        "CELEBRATION",
        "BABY CARE",
        "POULTRY",
        ])
        onpromotion = col1.slider("total number of items in a product family that were being promoted at a store at a given date", min_value=0, value=741) 
        oil_prices = col1.slider("What is the current price of oil?",min_value=26.19, value=110.62)
        city = col1.selectbox("which city is the store located", options=[
        "Quito",
        "Guayaquil",
        "Santo Domingo",
        "Cuenca",
        "Ambato",
        "Manta",
        "Latacunga",
        "Machala",
        "Daule",
        "Puyo",
        "Libertad",
        "Cayambe",
        "Guaranda",
        "El Carmen",
        "Quevedo",
        "Babahoyo",
        "Playas",
        "Ibarra",
        "Riobamba",
        "Loja",
        "Salinas",
        "Esmeraldas"
        ])
        state = col1.selectbox("Which state is the store located?", options=[
        "Pichincha",
        "Guayas",
        "Santo Domingo de los Tsachilas",
        "Azuay",
        "Manabi",
        "Tungurahua",
        "Los Rios",
        "Cotopaxi",
        "El Oro",
        "Pastaza",
        "Bolivar",
        "Imbabura",
        "Chimborazo",
        "Loja",
        "Santa Elena",
        "Esmeraldas"
        ])

        # set up col2
        col2.write("Inputs Part 2:")
        stores_type = col2.radio("What is the type of the store?", options=['A','B','C','D','E'])
        cluster = col2.number_input("what is the cluster of the store", min_value=1, max_value=17)
        Year = col2.number_input("Enter a year", min_value=2013, step=1)
        Month = col2.number_input("Enter the month",min_value=1, step=1)
        Day = col2.number_input("Enter the day of the month", min_value=1, step=1)

        # Create the submit button
        submitted = form.form_submit_button("Submit")


# Upon submission
if submitted:
    with predictions:
        # Format inputs
        input_dict = {
            "store_nbr" : [store_nbr],
            "product" : [product],
            "onpromotion" : [onpromotion],
            "oil_prices" : [oil_prices],
            "city" : [city],
            "state" : [state],
            "stores_type" : [stores_type],
            "cluster" : [cluster],
            "Year" : [Year],
            "Month" : [Month],
            "Day" : [Day]

        }

        # Convert to a dataframe
        input_data = pd.DataFrame.from_dict(input_dict)

        # Transform inputs to one-hot encoded format for the specified columns
        encoded_test_cat = encoder.transform(input_data[cat_columns])

        # Get the feature names from the encoder
        feature_names = encoder.get_feature_names_out(input_features=cat_columns)

        # Create a DataFrame using the encoded data and feature names
        encoded_tcat = pd.DataFrame(encoded_test_cat, columns=feature_names)

        # Concatenate the one-hot encoded DataFrame and the remaining columns
        # Get a list of columns that were not one-hot encoded
        remaining_columns = [col for col in input_data.columns if col not in cat_columns]

        # Concatenate the one-hot encoded DataFrame and the remaining columns using the 'concat' method
        input_data = pd.concat([encoded_tcat, input_data[remaining_columns]], axis=1)


        # Make the prediction
        model_output = model.predict(input_data)
        input_data["predictions"] = model_output

    
        predicted_sales = model_output
        
        # Convert the list of predictions to a comma-separated string with two decimal places
        predicted_sales_str = ', '.join([f'{value:,.2f}' for value in predicted_sales])



    
    # Display the predictions
    st.success(f"Prediction for Sales: ${predicted_sales_str}")
    