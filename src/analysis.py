
import pandas as pd


def calculate_summary(df):
    income = df.loc[df["Type"] == "Income", "Amount"].sum()
    expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()

    return {
        "total_income": float(income),
        "total_expenses": float(expenses),
        "net_balance": float(income - expenses),
        "total_transactions": int(len(df))
    }


def category_analysis(df):
    expenses = df[df["Type"] == "Expense"]

    return (
        expenses.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def monthly_analysis(df):
    data = df.copy()
    data["Month"] = data["Date"].dt.to_period("M").astype(str)

    result = (
        data.pivot_table(
            index="Month",
            columns="Type",
            values="Amount",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
        .sort_values("Month")
    )

    for column in ["Income", "Expense"]:
        if column not in result.columns:
            result[column] = 0

    return result


def payment_analysis(df):
    expenses = df[df["Type"] == "Expense"]

    return (
        expenses.groupby("Payment_Method")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def weekday_analysis(df):
    expenses = df[df["Type"] == "Expense"].copy()
    expenses["Weekday"] = expenses["Date"].dt.day_name()

    return (
        expenses.groupby("Weekday")["Amount"]
        .sum()
        .reset_index()
    )
