import streamlit as st
from engine import SaasEconomicsModel
import pandas as pd

# Настройка страницы
st.set_page_config(
    page_title="SaaS Profit Simulator",
    page_icon="🚀",
    layout="wide"
)

# Скрываем меню и подвал Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📊 SaaS Unit Economics & Profit Simulator")
st.markdown("""
This tool simulates the financial path of a SaaS platform based on your business metrics. 
Adjust the sliders on the left to see how **Churn Rate** and **CAC** impact your break-even point.
""")

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

    st.info("💡 **What-If Scenario:** Change the Churn Rate to see how fast the profit grows!")


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
col4.metric("LTV", f"${ltv:,.0f}", help="Lifetime Value per Customer")

st.divider()


st.subheader("📈 Financial Trajectory")


chart_data = df.set_index('Month')[['Cumulative_Profit', 'Revenue']]


st.area_chart(df.set_index('Month')['Cumulative_Profit'])


st.subheader("🎯 Insights")

be_month = df[df['Cumulative_Profit'] >= 0]['Month'].min()

if pd.isna(be_month):
    st.error(
        "⚠️ With these settings, your business remains in deficit for at least 24 months. Try reducing CAC or Churn.")
else:
    st.success(f"✅ Your business reaches the **Break-Even Point** in month **{int(be_month)}**.")


with st.expander("See Raw Simulation Data"):
    st.dataframe(df.style.format(precision=0), use_container_width=True)

st.markdown("---")
st.caption("Developed as a Portfolio Project | Unit Economics Simulator v1.0")
