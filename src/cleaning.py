
import pandas as pd


REQUIRED_COLUMNS = [
    "Date", "Category", "Description",
    "Amount", "Type", "Payment_Method"
]


def clean_data(df):
    df = df.copy()

    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    df["Category"] = df["Category"].fillna("Other").astype(str)
    df["Description"] = df["Description"].fillna("No description")
    df["Type"] = df["Type"].fillna("Expense").astype(str).str.title()
    df["Payment_Method"] = (
        df["Payment_Method"].fillna("Unknown").astype(str)
    )

    df = df.dropna(subset=["Date", "Amount"])
    df = df[df["Amount"] > 0]
    df = df[df["Type"].isin(["Income", "Expense"])]

    df = df.drop_duplicates()
    df = df.sort_values("Date").reset_index(drop=True)

    return df
