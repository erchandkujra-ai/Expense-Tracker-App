
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="💰",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "expenses.csv"
BUDGET_FILE = DATA_DIR / "budgets.csv"

# ---------------------------------
# LOAD DARK BLUE CSS
# ---------------------------------
css_file = BASE_DIR / "style.css"

if css_file.exists():
    with open(css_file, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ---------------------------------
# DATA FUNCTIONS
# ---------------------------------
REQUIRED_COLUMNS = [
    "Date", "Category", "Description",
    "Amount", "Type", "Payment_Method"
]


def load_data():
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            if all(col in df.columns for col in REQUIRED_COLUMNS):
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
                df = df.dropna(subset=["Date", "Amount"])
                df = df[df["Amount"] >= 0]
                df["Type"] = df["Type"].astype(str).str.title()
                return df[REQUIRED_COLUMNS].copy()
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass

    return pd.DataFrame(columns=REQUIRED_COLUMNS)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def load_budgets():
    if BUDGET_FILE.exists() and BUDGET_FILE.stat().st_size > 0:
        try:
            budgets = pd.read_csv(BUDGET_FILE)
            if {"Category", "Budget"}.issubset(budgets.columns):
                budgets["Budget"] = pd.to_numeric(
                    budgets["Budget"], errors="coerce"
                )
                return budgets.dropna(subset=["Budget"])
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass

    return pd.DataFrame(columns=["Category", "Budget"])


# ---------------------------------
# SESSION STATE
# ---------------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()

if "budgets" not in st.session_state:
    st.session_state.budgets = load_budgets()

# ---------------------------------
# HEADER
# ---------------------------------
st.title("💰 Expense Tracker Dashboard")
st.caption(
    "Personal Finance Analytics | Income, Expenses & Budget Monitoring"
)

st.divider()

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.title("⚙️ Dashboard Controls")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Add Transaction",
        "Budget Manager",
        "Upload / Export Data"
    ]
)

df = st.session_state.transactions.copy()

# ---------------------------------
# DASHBOARD PAGE
# ---------------------------------
if page == "Dashboard":

    st.subheader("📊 Financial Overview")

    if df.empty:
        st.info(
            "No transactions found. Add a transaction or upload a CSV file."
        )
        st.stop()

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        categories = ["All"] + sorted(
            df["Category"].dropna().astype(str).unique().tolist()
        )
        selected_category = st.selectbox(
            "Filter by Category", categories
        )

    with col2:
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()

        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date)
        )

    filtered = df.copy()

    if selected_category != "All":
        filtered = filtered[
            filtered["Category"] == selected_category
        ]

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["Date"].dt.date >= start_date)
            & (filtered["Date"].dt.date <= end_date)
        ]

    income = filtered.loc[
        filtered["Type"] == "Income", "Amount"
    ].sum()

    expenses = filtered.loc[
        filtered["Type"] == "Expense", "Amount"
    ].sum()

    balance = income - expenses

    # KPI Cards
    c1, c2, c3 = st.columns(3)

    c1.metric("💵 Total Income", f"₹{income:,.2f}")
    c2.metric("💸 Total Expenses", f"₹{expenses:,.2f}")
    c3.metric("🏦 Net Balance", f"₹{balance:,.2f}")

    st.divider()

    expense_df = filtered[filtered["Type"] == "Expense"].copy()
    income_df = filtered[filtered["Type"] == "Income"].copy()

    # Charts
    left, right = st.columns(2)

    with left:
        st.subheader("Category-wise Expenses")

        if not expense_df.empty:
            category_data = (
                expense_df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                category_data,
                names="Category",
                values="Amount",
                hole=0.45,
                title="Expense Distribution",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expense data available.")

    with right:
        st.subheader("Monthly Income vs Expenses")

        if not filtered.empty:
            monthly = filtered.copy()
            monthly["Month"] = monthly["Date"].dt.to_period(
                "M"
            ).astype(str)

            monthly_data = (
                monthly.groupby(["Month", "Type"])["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                monthly_data,
                x="Month",
                y="Amount",
                color="Type",
                barmode="group",
                template="plotly_dark",
                title="Monthly Financial Trend"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No monthly data available.")

    st.divider()

    # Payment analysis
    st.subheader("💳 Payment Method Analysis")

    if not expense_df.empty:
        payment_data = (
            expense_df.groupby("Payment_Method")["Amount"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            payment_data,
            x="Payment_Method",
            y="Amount",
            color="Payment_Method",
            template="plotly_dark",
            title="Spending by Payment Method"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No payment data available.")

    # Budget warnings
    st.divider()
    st.subheader("⚠️ Budget Monitoring")

    budgets = st.session_state.budgets

    if not budgets.empty:
        if not expense_df.empty:
            category_spending = (
                expense_df.groupby("Category")["Amount"]
                .sum()
            )

            for _, row in budgets.iterrows():
                category = row["Category"]
                budget = float(row["Budget"])
                spent = float(category_spending.get(category, 0))
                utilization = spent / budget if budget > 0 else 0

                st.write(
                    f"**{category}: ₹{spent:,.2f} / ₹{budget:,.2f}**"
                )

                st.progress(min(utilization, 1.0))

                if utilization > 1:
                    st.error(
                        f"{category}: Budget exceeded by "
                        f"₹{spent - budget:,.2f}"
                    )
                elif utilization >= 0.8:
                    st.warning(
                        f"{category}: You have used "
                        f"{utilization * 100:.1f}% of your budget."
                    )
                else:
                    st.success("Budget is within limit.")
        else:
            st.info("No expenses available for budget analysis.")
    else:
        st.info("Add category budgets from Budget Manager.")

    # Transaction table
    st.divider()
    st.subheader("📋 Transaction History")

    st.dataframe(
        filtered.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------
# ADD TRANSACTION PAGE
# ---------------------------------
elif page == "Add Transaction":

    st.subheader("➕ Add New Transaction")

    with st.form("transaction_form"):
        date = st.date_input("Transaction Date")
        category = st.selectbox(
            "Category",
            [
                "Food", "Travel", "Shopping", "Bills",
                "Education", "Health", "Entertainment",
                "Salary", "Business", "Other"
            ]
        )

        description = st.text_input("Description")
        amount = st.number_input(
            "Amount (₹)", min_value=0.0, step=100.0
        )

        transaction_type = st.selectbox(
            "Transaction Type", ["Expense", "Income"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "UPI", "Card", "Bank Transfer", "Other"]
        )

        submitted = st.form_submit_button("Save Transaction")

        if submitted:
            if amount <= 0:
                st.error("Please enter an amount greater than zero.")
            else:
                new_transaction = pd.DataFrame([{
                    "Date": pd.Timestamp(date),
                    "Category": category,
                    "Description": description,
                    "Amount": amount,
                    "Type": transaction_type,
                    "Payment_Method": payment_method
                }])

                updated = pd.concat(
                    [st.session_state.transactions, new_transaction],
                    ignore_index=True
                )

                st.session_state.transactions = updated
                save_data(updated)

                st.success("Transaction saved successfully!")
                st.rerun()

# ---------------------------------
# BUDGET MANAGER PAGE
# ---------------------------------
elif page == "Budget Manager":

    st.subheader("🎯 Monthly Budget Manager")

    with st.form("budget_form"):
        budget_category = st.selectbox(
            "Select Category",
            [
                "Food", "Travel", "Shopping", "Bills",
                "Education", "Health", "Entertainment", "Other"
            ]
        )

        budget_amount = st.number_input(
            "Set Budget (₹)", min_value=0.0, step=500.0
        )

        budget_submit = st.form_submit_button("Save Budget")

        if budget_submit:
            if budget_amount <= 0:
                st.error("Budget must be greater than zero.")
            else:
                budgets = st.session_state.budgets.copy()

                budgets = budgets[
                    budgets["Category"] != budget_category
                ]

                new_budget = pd.DataFrame([{
                    "Category": budget_category,
                    "Budget": budget_amount
                }])

                budgets = pd.concat(
                    [budgets, new_budget], ignore_index=True
                )

                st.session_state.budgets = budgets
                budgets.to_csv(BUDGET_FILE, index=False)

                st.success("Budget saved successfully!")
                st.rerun()

    st.divider()
    st.subheader("Current Budgets")

    if not st.session_state.budgets.empty:
        st.dataframe(
            st.session_state.budgets,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No budgets created yet.")

# ---------------------------------
# UPLOAD / EXPORT PAGE
# ---------------------------------
elif page == "Upload / Export Data":

    st.subheader("📂 Upload Transaction CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)

            missing = [
                col for col in REQUIRED_COLUMNS
                if col not in uploaded_df.columns
            ]

            if missing:
                st.error(
                    "Missing columns: " + ", ".join(missing)
                )
            else:
                uploaded_df["Date"] = pd.to_datetime(
                    uploaded_df["Date"], errors="coerce"
                )
                uploaded_df["Amount"] = pd.to_numeric(
                    uploaded_df["Amount"], errors="coerce"
                )
                uploaded_df = uploaded_df.dropna(
                    subset=["Date", "Amount"]
                )
                uploaded_df = uploaded_df[
                    uploaded_df["Amount"] >= 0
                ]

                uploaded_df["Type"] = (
                    uploaded_df["Type"].astype(str).str.title()
                )

                uploaded_df = uploaded_df[
                    uploaded_df["Type"].isin(["Income", "Expense"])
                ]

                if st.button("Import CSV Data"):
                    st.session_state.transactions = uploaded_df[
                        REQUIRED_COLUMNS
                    ].copy()

                    save_data(st.session_state.transactions)
                    st.success("CSV data imported successfully!")
                    st.rerun()

                st.write("Preview:")
                st.dataframe(
                    uploaded_df.head(10),
                    use_container_width=True
                )

        except Exception as error:
            st.error(f"Unable to read CSV: {error}")

    st.divider()
    st.subheader("📥 Export Transactions")

    if not st.session_state.transactions.empty:
        export_df = st.session_state.transactions.copy()

        csv_data = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Transactions CSV",
            data=csv_data,
            file_name="expense_tracker_export.csv",
            mime="text/csv"
        )
    else:
        st.info("No transaction data available to export.")

# ---------------------------------
# FOOTER
# ---------------------------------
st.divider()
st.caption(
    "Expense Tracker App | Built with Python, Pandas, "
    "Plotly and Streamlit"
)
