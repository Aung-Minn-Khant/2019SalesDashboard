import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

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


city_total_pie=px.pie(
    df_select,
    values='Total',
    names='Month',
    title='Total Sales By Month'
    )
c_col.plotly_chart(city_total_pie,user_container_wide=True)


df['OrderDate']=pd.to_datetime(df['OrderDate']).dt.date
chosen_date = st.date_input("Choose the date from 2019-01-01 to 2020-01-01 to show total sales by cities.",
                            datetime.date(2019,1,1),format="YYYY-MM-DD")
total=df[df['OrderDate']==chosen_date].groupby('City')['Total'].sum()



d_col,e_col=st.columns(2)

sales_by_city=df_select.groupby('City')['Total'].sum().sort_values(ascending=True)
dfmonth_fig=px.line(
    df_select,
    x=sales_by_city.index,
    y=sales_by_city.values,
    title="Total sales by city"
)
d_col.plotly_chart(dfmonth_fig,user_container_wide=True)

orderqtybycity_inchosendate=px.bar(
    total,
    x=total.index,
    y=total.values,
    orientation='v',
    title="Total sales in all cities by chosen date"
)
e_col.plotly_chart(orderqtybycity_inchosendate,user_container_wide=True)

st.title("2019 Sales Dataset")
st.write(df)
