import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Veridi Delivery Audit", layout="wide")
st.title("Last Mile Logistics Auditor — Veridi Logistics")
st.caption("Auditing delivery performance and its impact on customer sentiment")

df = pd.read_csv('cleaned_delivery_data.csv')

st.header("📍 % Late Deliveries by State")
state_pct = (
    df.groupby('customer_state')['delivery_status']
    .apply(lambda x: (x != 'On Time').mean() * 100)
    .reset_index(name='pct_late')
    .sort_values('pct_late', ascending=False)
)
fig1 = px.bar(state_pct, x='customer_state', y='pct_late',
              labels={'pct_late': '% Late', 'customer_state': 'State'})
st.plotly_chart(fig1, use_container_width=True)

st.header("⭐ Review Score vs Delivery Status")
avg_score = df.groupby('delivery_status')['review_score'].mean().reset_index()
fig2 = px.bar(avg_score, x='delivery_status', y='review_score',
              labels={'review_score': 'Avg Review Score (1-5)'})
st.plotly_chart(fig2, use_container_width=True)

st.header("📉 Delay vs Review Score")
fig3 = px.scatter(df, x='Days_Difference', y='review_score', opacity=0.3,
                   trendline='ols',
                   labels={'Days_Difference': 'Days Difference (negative = late)'})
st.plotly_chart(fig3, use_container_width=True)

st.header("📦 % Late by Product Category (min 50 orders)")
cat_pct = (
    df.groupby('product_category_name_english')['delivery_status']
    .apply(lambda x: (x != 'On Time').mean() * 100)
    .reset_index(name='pct_late')
)
cat_vol = df.groupby('product_category_name_english').size().reset_index(name='order_count')
cat_summary = cat_pct.merge(cat_vol, on='product_category_name_english')
cat_summary = cat_summary[cat_summary['order_count'] >= 50].sort_values('pct_late', ascending=False).head(15)
fig4 = px.bar(cat_summary, x='product_category_name_english', y='pct_late',
              hover_data=['order_count'])
st.plotly_chart(fig4, use_container_width=True)