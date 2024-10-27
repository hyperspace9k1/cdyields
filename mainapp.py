# Streamlit app for cost-benefit analysis of CDs vs. Treasuries

import streamlit as st

# Mock data for state tax rates by state and income bracket (in percentage)
state_tax_rates = {
    "California": {"low_income": 1, "mid_income": 6, "high_income": 9.3},
    "Texas": {"low_income": 0, "mid_income": 0, "high_income": 0},
    "New York": {"low_income": 4, "mid_income": 6.33, "high_income": 8.82},
    "Florida": {"low_income": 0, "mid_income": 0, "high_income": 0},
    "Illinois": {"low_income": 4.95, "mid_income": 4.95, "high_income": 4.95},
}

# Federal tax brackets (in percentage)
federal_tax_brackets = {
    "10%": 10,
    "12%": 12,
    "22%": 22,
    "24%": 24,
    "32%": 32,
    "35%": 35,
    "37%": 37
}

# Define the function for the analysis
def enhanced_cd_vs_treasury_analysis(treasury_yield, cd_yield, federal_bracket, state, income_bracket):
    # Convert yields and tax rates to decimal
    treasury_yield /= 100
    cd_yield /= 100
    federal_tax_rate = federal_tax_brackets.get(federal_bracket, 0) / 100
    state_tax_rate = state_tax_rates.get(state, {}).get(income_bracket, 0) / 100

    # Calculate after-tax yields
    after_tax_treasury_yield = treasury_yield * (1 - federal_tax_rate)
    after_tax_cd_yield = cd_yield * (1 - federal_tax_rate) * (1 - state_tax_rate)

    # Calculate the premium needed by CD over Treasury
    cd_premium = after_tax_treasury_yield - after_tax_cd_yield
    recommendation = "Invest in CD" if after_tax_cd_yield > after_tax_treasury_yield else "Invest in Treasury"

    return after_tax_treasury_yield * 100, after_tax_cd_yield * 100, cd_premium * 100, recommendation

# Streamlit app interface
st.title("CD vs Treasury Cost-Benefit Analysis")

# Input fields
treasury_yield = st.number_input("Treasury Yield (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
cd_yield = st.number_input("CD Yield (%)", min_value=0.0, max_value=20.0, value=6.0, step=0.1)
federal_bracket = st.selectbox("Federal Tax Bracket", options=list(federal_tax_brackets.keys()))
state = st.selectbox("State", options=list(state_tax_rates.keys()))
income_bracket = st.selectbox("Income Level", options=["low_income", "mid_income", "high_income"])

# Perform calculation when button is clicked
if st.button("Calculate"):
    after_tax_treasury_yield, after_tax_cd_yield, cd_premium, recommendation = enhanced_cd_vs_treasury_analysis(
        treasury_yield, cd_yield, federal_bracket, state, income_bracket
    )

    # Display the results
    st.write("### Results")
    st.write(f"After-Tax Treasury Yield: {after_tax_treasury_yield:.2f}%")
    st.write(f"After-Tax CD Yield: {after_tax_cd_yield:.2f}%")
    st.write(f"CD Premium Over Treasury: {cd_premium:.2f}%")
    st.write(f"**Recommendation:** {recommendation}")
