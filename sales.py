import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import seaborn as sb

st.set_page_config(page_title="My Sale Dashboard",page_icon=":bar_chart:",layout="wide")
df=pd.read_csv("all_df.csv")

product = st.sidebar.multiselect("Select product",
                      options=df['Product'].unique(),
                       default=df['Product'].unique()[:3]
                      )
city = st.sidebar.multiselect("Select City",
                      options=df['City'].unique(),
                       default=df['City'].unique()[:3]
                      )
month = st.sidebar.multiselect("Select Month",
                      options=df['Month'].unique(),
                       default=df['Month'].unique()[:3]
                      )

st.title(":bar_chart: Sales Dasbboard 2019")
st.markdown("##")

total_sales=df['Total'].sum()
product_num=df["Product"].nunique()

left,right=st.columns(2)
with left:
    st.subheader("Total Sales")
    st.subheader(f' US $ {total_sales}')
with right:
    st.subheader("Number of Products")
    st.subheader(f'{product_num}')

df_select=df.query("City==@city and Product==@product and Month==@month")
sales_by_product=df_select.groupby('Product')['Total'].sum().sort_values()
sales_chart=px.bar(
    sales_by_product,
    x=sales_by_product.values,
    y=sales_by_product.index,
    orientation='h',
    title='Sales by Product'
    
)

a_col,b_col,c_col=st.columns(3)
a_col.plotly_chart(sales_chart,user_container_wide=True)


item_qty_by_city=df_select.groupby('City')['QuantityOrdered'].sum().sort_values()
qty_chart=px.bar(
    item_qty_by_city,
    x=item_qty_by_city.values,
    y=item_qty_by_city.index,
    orientation='h',
    title='Total Quantity By City'
    
)

b_col.plotly_chart(qty_chart,user_container_wide=True)


city_total=df_select.groupby('City')['Total'].sum().sort_values()
city_total_pie=px.pie(
    df_select,
    values='Total',
    names='Month',
    title='Total Sales By Month'
    )
c_col.plotly_chart(city_total_pie,user_container_wide=True)
st.title("Total order quantity of cities by dates")
df['OrderDate']=pd.to_datetime(df['OrderDate']).dt.date

chosen_date = st.date_input("Choose the date from 2019-01-01 to 2020-01-01 to show total order quantity by cities.",
                            datetime.date(2019,1,1),format="YYYY-MM-DD")

total=df[df['OrderDate']==chosen_date].groupby('City')['Total'].sum()
sb.barplot(x=total.index,y=total.values)
sb.set_theme(context='notebook', style='darkgrid', palette='deep', font='sans-serif', font_scale=1, color_codes=True, rc=None)
plt.xticks(rotation=90)
plt.xlabel("Cities")
plt.ylabel("Total qty")
st.pyplot(plt.gcf())

st.title("2019 Sales Dataset")
st.write(df)
