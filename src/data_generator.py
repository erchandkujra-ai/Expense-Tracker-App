
import numpy as np
import pandas as pd
from pathlib import Path


def generate_data(rows=1000, seed=42):
    np.random.seed(seed)

    categories = [
        "Food", "Travel", "Shopping", "Bills",
        "Healthcare", "Entertainment", "Education"
    ]

    payment_methods = ["Cash", "UPI", "Card", "Net Banking"]

    dates = pd.date_range(
        start="2025-01-01",
        end="2025-12-31",
        freq="D"
    )

    data = pd.DataFrame({
        "Date": np.random.choice(dates, rows),
        "Category": np.random.choice(
            categories, rows,
            p=[0.25, 0.15, 0.15, 0.15, 0.08, 0.12, 0.10]
        ),
        "Description": np.random.choice(
            ["Monthly purchase", "Daily payment", "Online order",
             "Personal expense", "Regular transaction"],
            rows
        ),
        "Amount": np.round(np.random.uniform(50, 5000, rows), 2),
        "Type": np.random.choice(
            ["Expense", "Income"], rows, p=[0.85, 0.15]
        ),
        "Payment_Method": np.random.choice(payment_methods, rows)
    })

    data["Date"] = pd.to_datetime(data["Date"])
    return data.sort_values("Date").reset_index(drop=True)


def save_data():
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    df = generate_data()
    df.to_csv(data_dir / "expenses.csv", index=False)

    budgets = pd.DataFrame({
        "Category": [
            "Food", "Travel", "Shopping", "Bills",
            "Healthcare", "Entertainment", "Education"
        ],
        "Budget": [5000, 3000, 4000, 3500, 2500, 2000, 3000]
    })

    budgets.to_csv(data_dir / "budgets.csv", index=False)

    print("Synthetic expense data generated successfully!")
    print(f"Transactions: {len(df)}")


if __name__ == "__main__":
    save_data()
