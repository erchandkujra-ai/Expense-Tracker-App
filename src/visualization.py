
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def create_visualizations(df, category_data, monthly_data):
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    sns.set_theme(style="whitegrid")

    # Category spending chart
    if not category_data.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=category_data,
            x="Amount",
            y="Category"
        )
        plt.title("Expense by Category")
        plt.xlabel("Amount")
        plt.ylabel("Category")
        plt.tight_layout()
        plt.savefig(output_dir / "category_spending.png")
        plt.close()

    # Monthly income and expense chart
    if not monthly_data.empty:
        plt.figure(figsize=(11, 6))

        plt.plot(
            monthly_data["Month"],
            monthly_data["Income"],
            marker="o",
            label="Income"
        )

        plt.plot(
            monthly_data["Month"],
            monthly_data["Expense"],
            marker="o",
            label="Expense"
        )

        plt.title("Monthly Income vs Expenses")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / "monthly_income_expense.png")
        plt.close()

    # Expense distribution
    if not category_data.empty:
        plt.figure(figsize=(8, 8))
        plt.pie(
            category_data["Amount"],
            labels=category_data["Category"],
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Expense Distribution")
        plt.tight_layout()
        plt.savefig(output_dir / "expense_distribution.png")
        plt.close()

    print("Charts saved inside outputs folder.")
