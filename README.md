# PetroPulse: Ethiopia Fuel Intelligence & Landed Cost Engine
[![Live Demo](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)]()

### A Real-Time Decision Support System for National Fuel Procurement and Margin Analysis

---

## Description
PetroPulse is a specialized analytics platform designed to bridge the gap between global oil market volatility and the regulated Ethiopian energy landscape.  

As of April 2026, Ethiopia faces unique challenges including the floating of the Birr (ETB) and regional supply chain shocks. This tool automates the calculation of Landed Costs (CIF) and provides a "Live Gap Analysis" comparing actual import costs against the Ministry of Trade and Regional Integration (MoTRI) retail caps.

---

## The Problem
The Ethiopian fuel distribution sector is currently navigating a "Triple Threat" crisis:

### 1. Currency Volatility
The floating ETB/USD exchange rate creates a moving target for importers, where a 1% shift in currency can result in millions of Birr in unbudgeted costs.

### 2. Logistics Disruptions
Regional instability in the Red Sea and the Strait of Hormuz has spiked freight premiums and insurance rates, significantly increasing the Landed Cost above global Brent Crude benchmarks.

### 3. Subsidy Pressure
Large discrepancies between the global "True Cost" and the regulated "Pump Price" lead to massive over/under-recoveries, threatening the liquidity of national energy enterprises.

---

## The Solution
An end-to-end data pipeline and interactive dashboard that:

- **Automates Data Ingestion**  
  Uses `yfinance` to pull live Brent Crude and RBOB Gasoline futures.

- **Landed Cost Engine**  
  Custom mathematical model to calculate CIF (Cost, Insurance, and Freight) including:
  - Exchange rates  
  - Maritime risk premiums  
  - Import duties  

- **Margin Intelligence**  
  Real-time tracking of the "Subsidy Gap":
  - Over-recovery state  
  - Subsidy state  

- **Risk Modeling**  
  Integrated 20-day Moving Average (SMA) to:
  - Filter market noise  
  - Identify optimal procurement windows  

- **What-If Simulation**  
  Interactive UI enabling executives to simulate:
  - Birr devaluation  
  - Freight cost spikes  
  - Impact on national fuel bill  

---

## Strategic Recommendations
Based on market analysis as of **April, 2026**:

### 1. Hedge Against Currency Risk
With the current over-recovery period:
- Maximize import quotas  
- Build a Strategic Reserve before further currency adjustments  

### 2. Logistics Diversification
Due to disruption in the Hormuz corridor:
- Shift to alternative supply routes  
- Secure long-term charter agreements  

### 3. Dynamic Pricing Advocacy
Leverage platform insights to:
- Advocate for bi-weekly fuel price adjustments (instead of monthly)  
- Reduce financial shocks during supply spikes  

---

## Tech Stack

| Category            | Tools / Technologies |
|--------------------|---------------------|
| **Language**        | Python 3.10+        |
| **Dashboard**       | Streamlit           |
| **Data Science**    | Pandas, NumPy       |
| **Visualization**   | Plotly              |
| **Financial Data**  | YFinance API        |
| **Analysis**        | Jupyter Notebook    |

---

## Use Cases
- National fuel procurement planning  
- Import cost optimization  
- Policy simulation & subsidy analysis  
- Executive decision support  

---

## Future Enhancements
- Integration with real-time FX APIs (ETB/USD)  
- AI-based price forecasting models  
- Multi-country fuel benchmarking  
- Alert system for cost threshold breaches  

---

## Author
**Aklilu Abera**  | Supply Chain Data Analyst  

---

## Disclaimer
This tool is designed for analytical and decision-support purposes only.  
Actual procurement decisions should consider official government policies and real-time market validations.

---
