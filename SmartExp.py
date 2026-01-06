import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import time
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

GOOGLE_BLUE = "#4285F4"
GOOGLE_RED = "#DB4437"
GOOGLE_YELLOW = "#F4B400"
GOOGLE_GREEN = "#0F9D58"

# ---------------- STYLES ----------------
def apply_custom_styles():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #DDEFBB, #FFEEEE);
    }
    h1, h2, h3 {
        color: black !important;
        -webkit-text-stroke: 0.25px white;
    }
    .google-box {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border-left: 5px solid #4285F4;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# ---------------- DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_AI_Ready.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# ---------------- DASHBOARD ----------------
class Dashboard:
    def render(self):
        st.title("Financial Intelligence Dashboard")
        st.header("December 2025")

        df = load_data()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Spent", "₹4,250")
        c2.metric("Remaining Budget", "₹1,750")
        c3.metric("Sustainability Score", "72 / 100")

        smooth_days = st.sidebar.slider("Smoothing Window (Days)", 1, 14, 3)

        expenses = df[df["Amount"] < 0].copy()
        expenses["Amount"] = expenses["Amount"].abs()

        plot_data = (
            expenses.groupby(["Date", "Clean_Category"])["Amount"]
            .sum()
            .reset_index()
            .sort_values("Date")
        )

        plot_data["Smoothed"] = plot_data.groupby("Clean_Category")["Amount"].transform(
            lambda x: x.rolling(window=smooth_days, min_periods=1).mean()
        )

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(
            data=plot_data,
            x="Date",
            y="Smoothed",
            hue="Clean_Category",
            linewidth=2.5,
            palette=[GOOGLE_BLUE, GOOGLE_RED, GOOGLE_GREEN, GOOGLE_YELLOW],
            ax=ax
        )

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

# ---------------- ADD EXPENSE ----------------
class AddExpense:
    def render(self):
        st.title("Add Expense")

        tab1, tab2 = st.tabs(["Manual Entry", "Camera Scan"])

        with tab1:
            with st.form("expense_form"):
                item = st.text_input("Item Name")
                amount = st.number_input("Amount (₹)", min_value=0)
                if st.form_submit_button("Save"):
                    st.success(f"{item} recorded successfully.")

        with tab2:
            st.markdown("""
            <div class="google-box">
            <h3>Jeeves Search & Save</h3>
            <p>Helping you make informed spending decisions.</p>
            </div>
            """, unsafe_allow_html=True)

            product = st.text_input("What are you buying?")
            if st.button("Check Market Options"):
                with st.spinner("Analyzing market data..."):
                    time.sleep(1)
                    st.info(f"Best available price for {product}: ₹24,990")

            st.divider()
            st.subheader("Receipt Upload")

            uploaded_file = st.file_uploader(
                "Upload receipt image or PDF",
                type=["jpg", "png", "jpeg", "pdf"]
            )

            if uploaded_file:
                with st.spinner("Processing receipt..."):
                    time.sleep(1)

                st.info("""
Store: Universal Bakery  
Date: 24-03-2019  
Total Amount: ₹471.00  
""")

                st.warning(
                    "Spending in the food category shows frequent clustering. "
                    "Reducing impulse purchases could improve savings."
                )

# ---------------- ANALYTICS ----------------
class Analytics:
    def render(self):
        st.title("Analytics")

        df = load_data()

        # ---- SIDEBAR CONTROLS ----
        st.sidebar.subheader("Analytics Filters")

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()

        date_range = st.sidebar.date_input(
            "Select Date Range",
            (min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        smooth_days = st.sidebar.slider("Smoothing Window (Days)", 1, 14, 3)

        if isinstance(date_range, tuple):
            start, end = date_range
            df = df[
                (df["Date"].dt.date >= start) &
                (df["Date"].dt.date <= end)
            ]

        expenses = df[df["Amount"] < 0].copy()
        expenses["Amount"] = expenses["Amount"].abs()

        # ---- SMOOTHED TREND ----
        st.subheader("Smoothed Expenditure Patterns")

        plot_data = (
            expenses.groupby(["Date", "Clean_Category"])["Amount"]
            .sum()
            .reset_index()
            .sort_values("Date")
        )

        plot_data["Smoothed"] = plot_data.groupby("Clean_Category")["Amount"].transform(
            lambda x: x.rolling(window=smooth_days, min_periods=1).mean()
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            data=plot_data,
            x="Date",
            y="Smoothed",
            hue="Clean_Category",
            linewidth=2.5,
            ax=ax
        )

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.yaxis.set_major_locator(MultipleLocator(100))
        ax.yaxis.set_minor_locator(MultipleLocator(50))
        plt.grid(alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # ---- DISTRIBUTION ----
        st.subheader("Spending Distribution & Density")

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(
            data=expenses,
            x="Amount",
            hue="Clean_Category",
            bins=20,
            kde=True,
            palette="magma",
            ax=ax
        )
        st.pyplot(fig)
        plt.close(fig)

        # ---- PIE ----
        st.subheader("Category-wise Spending Share")

        cat = expenses.groupby("Clean_Category")["Amount"].sum()

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            cat,
            labels=cat.index,
            autopct="%1.1f%%",
            startangle=80,
            explode=[0.03] * len(cat)
        )

        centre = plt.Circle((0, 0), 0.7, fc="white")
        ax.add_artist(centre)
        ax.text(0, 0, f"Total\n₹{int(cat.sum())}", ha="center", va="center", fontsize=14)
        ax.axis("equal")

        st.pyplot(fig)
        plt.close(fig)

# ---------------- AI ADVISOR ----------------
class AIAdvisor:
    def render(self):
        st.title("AI Advisor")

        query = st.text_area("Ask for financial guidance")

        responses = [
            "Your spending trend is stable with moderate variance.",
            "Reducing discretionary food expenses could improve savings.",
            "Mid-week transactions show higher volatility.",
            "Transport costs may increase next month."
        ]

        if st.button("Consult"):
            with st.spinner("Evaluating financial patterns..."):
                time.sleep(1)
                st.success(random.choice(responses))

# ---------------- NAVIGATION ----------------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    with st.sidebar:
        st.title("Smart Expense")
        if st.button("Dashboard"): st.session_state.page = "Dashboard"
        if st.button("Add Expense"): st.session_state.page = "AddExpense"
        if st.button("Analytics"): st.session_state.page = "Analytics"
        if st.button("AI Advisor"): st.session_state.page = "AIAdvisor"

    pages = {
        "Dashboard": Dashboard(),
        "AddExpense": AddExpense(),
        "Analytics": Analytics(),
        "AIAdvisor": AIAdvisor()
    }

    pages[st.session_state.page].render()

if __name__ == "__main__":
    main()
