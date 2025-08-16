# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,requests

# Write directly to the app
st.title(f"🥤Customize Your Smoothie!🥤 ")
st.write(
  "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("Name on your Smoothie will be :", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients: ",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string=', '.join (ingredients_list)
    
    for fruit_chosen in ingredients_list:
      ingredients_string+=fruit_chosen + ''
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
      sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True) 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values (? , ?)"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert=st.button("Submit order")
    if time_to_insert:
        session.sql(my_insert_stmt,params=[ingredients_string,name_on_order]).collect()
        st.success(f"🥤Your Smoothie is ordered,{name_on_order}!", icon="✅")


        
