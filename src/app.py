import streamlit as st
from engine import SaaSEconomicsModel
import pandas as pd

st.set_page_config(
    page_title="SaaS Profit Simulator",
    page_icon="🚀",
    layout="wide"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {display:none;}
            .block-container {padding-top: 2rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📊 SaaS Unit Economics & Profit Simulator")

st.divider()

st.sidebar.header("🕹️ Business Model Inputs")

with st.sidebar:
    st.subheader("Revenue & Growth")
    price = st.slider("Monthly Subscription Price ($)", 10, 500, 50)
    new_users = st.number_input("New Users per Month", 100, 10000, 500)

    st.subheader("Costs & Churn")
    cac = st.slider("Acquisition Cost (CAC) ($)", 5, 200, 40)
    churn = st.slider("Monthly Churn Rate (%)", 1, 50, 10) / 100
    fixed_costs = st.number_input("Monthly Fixed Costs ($)", 1000, 100000, 10000)

model = SaaSEconomicsModel(
    price=price,
    cac=cac,
    churn_rate=churn,
    fixed_costs=fixed_costs,
    new_users_per_month=new_users
)
df = model.calculate_simulation()

col1, col2, col3, col4 = st.columns(4)

final_profit = df['Cumulative_Profit'].iloc[-1]
total_users = df['Active_Users'].iloc[-1]
monthly_revenue = df['Revenue'].iloc[-1]

margin = price - 2.0
ltv = margin / churn if churn > 0 else 0

col1.metric("Net Profit (24m)", f"${final_profit:,.0f}")
col2.metric("Active Users", f"{total_users:,.0f}")
col3.metric("Monthly Revenue", f"${monthly_revenue:,.0f}")
col4.metric("LTV", f"${ltv:,.0f}")

st.divider()

st.subheader("📈 Financial Trajectory")
st.area_chart(df.set_index('Month')['Cumulative_Profit'])

st.subheader("🎯 Insights")
be_month = df[df['Cumulative_Profit'] >= 0]['Month'].min()

if pd.notna(be_month):
    st.success(f"✅ Break-even point reached in month **{int(be_month)}**")
else:
    st.error("❌ The project does not reach profit within 24 months.")
