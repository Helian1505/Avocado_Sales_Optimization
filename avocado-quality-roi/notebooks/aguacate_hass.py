"""Project 1: Avocado Sales Optimization
Phase 1: Synthetic Data Generation
This code simulates one year of daily avocado sales, factoring in losses due to low maturity."""

import pandas as pd
import numpy as np
from datetime import timedelta, date
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. ADJUSTED BUSINESS ASSUMPTIONS (BASED ON RESEARCH) ---
# Note: Daily Sales were adjusted to simulate a large supermarket chain
# to ensure the economic impact is significant enough to justify the investment.
DAILY_UNITS_BASE = 15000         # Potential daily sales (e.g., 15,000 units across a chain)
AVERAGE_PRICE_UNIT = 1000        # COP (Approximate price per unit)
ESTIMATED_REJECTION_RATE = 0.15  # 15% of customers do not buy due to quality/maturity.
LOW_MATURITY_THRESHOLD = 2.5     # Maturity level (1-5 scale) that triggers the rejection loss.

# --- 2. BASE DATA GENERATION ---
days = 365 # Simulate a full year
start_date = date(2025, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(days)]

df_avocado = pd.DataFrame({
    'Date': dates,
    # Simulate base demand with variation
    'Base_Demand': np.random.randint(DAILY_UNITS_BASE * 0.9, DAILY_UNITS_BASE * 1.1, days), 
    'Unit_Price_COP': AVERAGE_PRICE_UNIT, 
    # Simulate Maturity (Mean 3.2, Std Dev 0.7 - this creates days with low maturity fruit)
    'Gondola_Avg_Maturity': np.random.normal(3.2, 0.7, days).clip(1, 5).round(1) 
})

# --- 3. LOSS CALCULATION IN THE CURRENT SCENARIO ("WITHOUT MACHINE") ---

# 3.1. Calculate the Loss Ratio due to Low Maturity (if maturity is below the threshold)
# We assume that if maturity is below 2.5, the 15% rejection rate applies.
df_avocado['Maturity_Impact_Ratio'] = np.where(df_avocado['Gondola_Avg_Maturity'] < LOW_MATURITY_THRESHOLD, 
                                            ESTIMATED_REJECTION_RATE, 
                                            0)

# 3.2. Calculate Losses and Actual Sales
df_avocado['Units_Lost'] = df_avocado['Base_Demand'] * df_avocado['Maturity_Impact_Ratio']
df_avocado['Actual_Sales_Current'] = df_avocado['Base_Demand'] - df_avocado['Units_Lost']
df_avocado['Actual_Revenue_Current'] = df_avocado['Actual_Sales_Current'] * df_avocado['Unit_Price_COP']


print(f"Dataset generated with {len(df_avocado)} days of simulation.")
# print(df_avocado.head())


#Phase 2: Exploratory Data Analysis (EDA)
#This section quantifies the total loss and visually demonstrates the root cause.

pd.options.display.float_format = '{:,.0f}'.format # Format for easy viewing of large numbers

# Sum the total loss
total_units_lost = df_avocado['Units_Lost'].sum()
total_revenue_loss = total_units_lost * AVERAGE_PRICE_UNIT

# Calculate percentage of lost units vs. total potential demand
total_base_demand = df_avocado['Base_Demand'].sum()
loss_percentage = (total_units_lost / total_base_demand) * 100

print("--- Current Scenario Financial Summary (1 Year) ---")
print(f"💰 Total Estimated Units Lost: {total_units_lost:,.0f}")
print(f"💸 Total Estimated Revenue Loss (COP): $ {total_revenue_loss:,.0f}")
print(f"📉 Percentage of Potential Demand Lost: {loss_percentage:.2f} %")
print("---------------------------------------------------")

#Root Cause Visualization (Scatter Plot)
# Plotting configuration
sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))

# Scatter Plot: Maturity vs. Loss
sns.scatterplot(x='Gondola_Avg_Maturity', y='Units_Lost', data=df_avocado)
plt.axvline(LOW_MATURITY_THRESHOLD, color='r', linestyle='--', label=f'Critical Threshold ({LOW_MATURITY_THRESHOLD})')
plt.title('Relationship between Avocado Maturity Level and Units Lost')
plt.xlabel('Average Maturity Level (Scale 1-5)')
plt.ylabel('Units Lost due to Rejection')
plt.legend()
plt.show()

#Phase 3: Solution Modeling and Financial Analysis (ROI)
#This code simulates the impact of implementing the grading machine and calculates the key financial metrics.
# Make sure to run the code from Phase 1 first so that 'df_avocado' exists.

# --- 1. FINANCIAL AND MACHINE EFFECTIVENESS ASSUMPTIONS ---
MACHINE_COST_COP = 150_000_000          # Estimated initial investment (COP $150 million)
DAILY_OPERATIONAL_COST = 150_000          # Daily operating cost (Labor, energy, maintenance)
SIMULATION_DAYS = len(df_avocado)        # 365 days
OPTIMIZED_REJECTION_RATE = 0.03          # The machine reduces loss from 15% to 3% on critical days.
AVERAGE_PRICE_UNIT = df_avocado['Unit_Price_COP'].iloc[0] # $1000 COP

# --- 2. SIMULATION OF THE "WITH MACHINE" SCENARIO ---

# 2.1. Calculate the Optimized Impact (new loss)
# The optimized impact only applies on days where maturity was a problem.
df_avocado['Optimized_Impact_Ratio'] = np.where(
    df_avocado['Maturity_Impact_Ratio'] > 0, # Only applies on days where there was loss (Maturity < 2.5)
    OPTIMIZED_REJECTION_RATE, 
    0
)

# 2.2. Calculate Units and Sales in the optimized scenario
df_avocado['Units_Lost_Optimized'] = df_avocado['Base_Demand'] * df_avocado['Optimized_Impact_Ratio']
df_avocado['Actual_Sales_Optimized'] = df_avocado['Base_Demand'] - df_avocado['Units_Lost_Optimized']
df_avocado['Actual_Revenue_Optimized'] = df_avocado['Actual_Sales_Optimized'] * df_avocado['Unit_Price_COP']

# --- 3. CALCULATION OF RECOVERY METRICS (BENEFIT) ---

# Units Recovered = Loss without machine - Loss with machine
df_avocado['Units_Recovered'] = df_avocado['Units_Lost'] - df_avocado['Units_Lost_Optimized']

# Revenue Recovered (Gross Benefit)
total_recovered_revenue = df_avocado['Units_Recovered'].sum() * AVERAGE_PRICE_UNIT


# --- 4. CALCULATION OF FINANCIAL METRICS (ROI and Payback) ---

# 4.1. Total Operational Cost (one year)
annual_operational_cost = DAILY_OPERATIONAL_COST * SIMULATION_DAYS

# 4.2. Net Benefit (Annual)
annual_net_benefit = total_recovered_revenue - annual_operational_cost

# 4.3. Return on Investment (ROI)
# ROI = (Annual Net Benefit / Machine Cost) * 100
annual_roi = (annual_net_benefit / MACHINE_COST_COP) * 100

# 4.4. Payback Period
# Payback = Initial Investment / Monthly Net Benefit (assuming constant flow)
monthly_net_benefit = annual_net_benefit / 12
payback_period_months = MACHINE_COST_COP / monthly_net_benefit

# --- 5. FINAL RESULTS FOR THE PORTFOLIO ---
print("\n" + "="*50)
print("             ✅ ANNUAL ECONOMIC ANALYSIS (OPTIMIZED SCENARIO)")
print("="*50)
# Use the Spanish formatting for COP for clarity in the context of the project
pd.options.display.float_format = '{:,.0f}'.format 
print(f"1. Avoided Revenue Loss (Gross Benefit): $ {total_recovered_revenue:,.0f} COP")
print(f"2. Annual Operational Cost:              $ {annual_operational_cost:,.0f} COP")
print(f"3. Annual Net Benefit Generated:         $ {annual_net_benefit:,.0f} COP")
print("-" * 50)
print(f"💰 Annual Project ROI:                  {annual_roi:,.2f} %")
print(f"⏱️ Payback Period:                      {payback_period_months:,.1f} months")
print("="*50 + "\n")


# --- 6. VISUALIZATION OF REVENUE COMPARISON ---

# Sum total revenues for both scenarios
current_total_revenue = df_avocado['Actual_Revenue_Current'].sum()
optimized_total_revenue = df_avocado['Actual_Revenue_Optimized'].sum()

# Create a DataFrame for the comparative chart
df_comparison = pd.DataFrame({
    'Scenario': ['Current (No Machine)', 'Optimized (With Machine)'],
    'Total_Annual_Revenue_COP': [current_total_revenue, optimized_total_revenue]
})

sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))
# Comparative Bar Chart of Total Revenues
ax = sns.barplot(x='Scenario', y='Total_Annual_Revenue_COP', data=df_comparison, palette=['red', 'green'])
plt.title('Total Annual Revenue: Current vs. Optimized')
plt.xlabel('Scenario')
plt.ylabel('Total Annual Revenue (COP)')

# Format Y-axis labels to display as millions
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: f'${x/1e6:,.0f}M')
)

plt.show()

df_avocado.to_csv('C:/Users/HF35_/Desktop/avocado-quality-roi/data/avocado_simulated_data.csv', index=False)