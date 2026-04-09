import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import get_market_data

# 1. Dashboard Configuration
st.set_page_config(page_title="PetroPulse Ethiopia - Executive Terminal", layout="wide")

# Custom CSS for a professional "Bloomberg-style" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    ...
    </style>
    """, unsafe_allow_html=True) 

# 3. Data Integration
st.sidebar.header("Market Benchmarks")

retail_diesel = st.sidebar.number_input("Retail Diesel Price (ETB/L)", value=163.09)
retail_gasoline = st.sidebar.number_input("Retail Gasoline Price (ETB/L)", value=142.41)

st.sidebar.divider()
st.sidebar.header("Landed Cost Engine")
etb_val = st.sidebar.number_input("Exchange Rate (USD/ETB)", value=154.58)
freight_val = st.sidebar.slider("Freight ($/Bbl)", 5.0, 50.0, 12.50)
ins_val = st.sidebar.slider("Insurance (%)", 0.5, 5.0, 1.5)
tax_val = st.sidebar.slider("Import Duty (%)", 0.0, 20.0, 5.0)

# Update the Function Definition to accept the retail price
@st.cache_data(ttl=3600)
def load_dashboard_data(etb_rate, freight_usd, insurance_val, duty_val, diesel_price):
    df = get_market_data()

    # Engine Logic
    df['Insurance_USD'] = df['Brent_Crude'] * (insurance_val / 100)
    df['CIF_USD'] = df['Brent_Crude'] + freight_usd + df['Insurance_USD']
    df['Landed_USD'] = df['CIF_USD'] * (1 + (duty_val / 100))

    # Unit Conversions
    LITERS_PER_BARREL = 158.98
    df['Landed_ETB_L'] = (df['Landed_USD'] * etb_rate) / LITERS_PER_BARREL

    # NEW: Calculate the Gap using the passed argument 'diesel_price'
    df['Subsidy_Gap'] = df['Landed_ETB_L'] - diesel_price
    df['MA20_Landed'] = df['Landed_ETB_L'].rolling(window=20).mean()

    return df

df = load_dashboard_data(etb_val, freight_val, ins_val, tax_val, retail_diesel)
latest = df.iloc[-1]

# 4. Header Section
st.title("🇪🇹 PetroPulse: Ethiopia Fuel Intelligence")
st.subheader(f"Market Status: Critical Supply Alert")

# 5. KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Landed Cost (ETB/L)", f"{latest['Landed_ETB_L']:.2f} Br")
with col2:
    # Inverse delta: red if positive (subsidy needed), green if negative (profit)
    delta_val = -latest['Subsidy_Gap'] 
    st.metric("Net Margin / Gap", f"{delta_val:.2f} Br", delta=f"{delta_val:.2f}")
with col3:
    st.metric("Brent Crude (USD)", f"${latest['Brent_Crude']:.2f}")
with col4:
    st.metric("Est. Daily Demand", "4.5M Liters", delta="-51%", delta_color="inverse")

# 6. Main Visualization
st.divider()
tab1, tab2, tab3 = st.tabs(["Margin Tracking", "Trading View (Risk)", "Supply Chain Risk"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Landed_ETB_L'], name="Landed Cost", line=dict(color='#00d1ff')))
    fig.add_hline(y=retail_diesel, line_dash="dash", line_color="#ff4b4b", annotation_text="Retail Price Cap")
    fig.update_layout(title="Landed Cost vs. Retail Cap (Last 90 Days)", template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Procurement Risk Intelligence")

    fig_trading = go.Figure()
    # Spot Price
    fig_trading.add_trace(go.Scatter(x=df.index, y=df['Landed_ETB_L'], 
                                     name="Spot Landed Cost", line=dict(color='#00d1ff', width=2)))
    # Moving Average
    fig_trading.add_trace(go.Scatter(x=df.index, y=df['MA20_Landed'], 
                                     name="20-Day Trend", line=dict(color='#ffaa00', width=2, dash='dot')))

    fig_trading.update_layout(title="Technical Trend: Spot vs. 20-Day Moving Average", 
                              template="plotly_dark", height=500,
                              hovermode="x unified")
    st.plotly_chart(fig_trading, use_container_width=True)

    # Risk Signal Logic
    last_price = df['Landed_ETB_L'].iloc[-1]
    last_ma = df['MA20_Landed'].iloc[-1]

    if last_price > last_ma:
        st.error(f" **MARKET OVERHEATED:** Current cost is {((last_price/last_ma)-1)*100:.1f}% above the 20-day average. Procurement risk is HIGH.")
    else:
        st.success(f" **BUYING WINDOW:** Current cost is below the 20-day average. Market is cooling; favorable for stockpiling.")

with tab3:
    st.subheader("Global Logistics & Supply Chain Risk")

    # 1. Critical Alert Banner
    st.error("""
    **EMERGENCY DIRECTIVE (April 2026):** National fuel supply has been cut by **51%** due to the Hormuz Corridor closure. 
    180,000 MT of contracted fuel is currently stalled in procurement.
    """)

    # 2. Risk Scorecard
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Route Status: Hormuz", "CLOSED", delta="-95% Traffic", delta_color="inverse")
    with col_b:
        st.metric("Daily Diesel Supply", "4.5M Liters", delta="Required: 9.2M")
    with col_c:
        st.metric("Spot Market Premium", "300%", delta="vs Long-term Contract")

    # 3. Priority Allocation Table (Per MoTRI Directive)
    st.divider()
    st.markdown("### Priority Allocation List ")
    st.info("The following sectors are currently prioritized for fuel distribution:")

    priority_data = {
        "Priority Rank": ["1", "2", "3", "4", "5"],
        "Sector": ["Public Transport & National Security", "Agricultural Tractors", "Export-Oriented Manufacturing", "Essential Consumer Goods Transport", "Major Infrastructure Projects"],
        "Status": ["Fully Prioritized", "Limited Supply", "Batch Delivery", "Scheduled Only", "On Hold"]
    }
    st.table(pd.DataFrame(priority_data))

    # 4. Strategic Supply Chart
    st.markdown("### Supply Volume Analysis")
    supply_chart = go.Figure(go.Bar(
        x=['Pre-Crisis (March)', 'Current (April)', 'Required'],
        y=[9.2, 4.5, 9.2],
        marker_color=['#00d1ff', '#ff4b4b', '#00d1ff']
    ))
    supply_chart.update_layout(title="Daily Diesel Supply Volume (Millions of Liters)", template="plotly_dark", height=350)
    st.plotly_chart(supply_chart, use_container_width=True)

    # 5. Inventory Recommendation
    st.warning("**Manager Action Required:** Divert all non-essential fleet operations. Monitor Djibouti-Addis corridor security as localized tensions may impact truck turnaround times.")

# 7. Strategic Recommendation
st.divider()
st.subheader("Strategic Advisory")
if latest['Subsidy_Gap'] > 10:
    st.error(f"**CRITICAL ACTION:** Landed cost ({latest['Landed_ETB_L']:.2f} Br) significantly exceeds retail price. Recommend immediate consultation with EPSE regarding subsidy disbursements.")
elif latest['Subsidy_Gap'] < -20:
    st.success("**WINDOW OF OPPORTUNITY:** High over-recovery detected. Recommend accelerating imports to build reserves before the next exchange rate adjustment.")
else:
    st.info("**STABLE MARGIN:** Maintain standard procurement cycles and monitor Red Sea freight volatility.")

st.divider()
st.caption(" **Developed by Aklilu Abera Dana** | **Supply Chain Data Analyst** | 2026")
