# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf

# Create a single Snowpark session
session = Session.builder.configs({
    "account": "VEICLSU-PC92155",
    "user": "MGRATZ2",
    "password": "6h#oiZgigEy2u3",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}).create()

# Define and register a UDF
@udf(session=session, return_type=IntegerType())
def my_udf(x: int) -> int:
    return x * 2


# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list =  st.multiselect(
    'Choose up to 5 ingredients: ', my_dataframe, max_selections=5
)

if ingredients_list:
     ingredients_string = ''
     for fuits_chosen in ingredients_list:
        ingredients_string += fuits_chosen + ' '
    # st.write(ingredients_string)
     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""
     time_to_insert = st.button('Submit Order')
     if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+ name_on_order, icon="✅")
