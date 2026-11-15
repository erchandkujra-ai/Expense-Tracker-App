
from pathlib import Path
import pandas as pd

from src.data_generator import save_data
from src.cleaning import clean_data
from src.analysis import (
    calculate_summary,
    category_analysis,
    monthly_analysis
)
from src.visualization import create_visualizations
from src.insights import generate_insights


def main():
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"
    output_dir = project_root / "outputs"

    # Generate sample data if it does not exist
    if not (data_dir / "expenses.csv").exists():
        save_data()

    # Load and clean data
    raw_data = pd.read_csv(data_dir / "expenses.csv")
    df = clean_data(raw_data)

    df.to_csv(data_dir / "cleaned_expenses.csv", index=False)

    # Load budgets
    budgets = pd.read_csv(data_dir / "budgets.csv")

    # Perform analysis
    summary = calculate_summary(df)
    categories = category_analysis(df)
    monthly = monthly_analysis(df)

    # Generate charts
    create_visualizations(df, categories, monthly)

    # Generate insights
    insights = generate_insights(summary, categories, budgets)

    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "insights.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(insights))

    print("\n========== EXPENSE TRACKER REPORT ==========")
    print(f"Total Income:   Rs. {summary['total_income']:,.2f}")
    print(f"Total Expenses: Rs. {summary['total_expenses']:,.2f}")
    print(f"Net Balance:    Rs. {summary['net_balance']:,.2f}")
    print(f"Transactions:   {summary['total_transactions']}")

    print("\n========== INSIGHTS ==========")
    for insight in insights:
        print("-", insight)

    print("\nProject analysis completed successfully!")
    print("Check the data and outputs folders.")


if __name__ == "__main__":
    main()
