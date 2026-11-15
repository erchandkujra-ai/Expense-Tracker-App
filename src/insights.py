
def generate_insights(summary, category_data, budgets):
    messages = []

    messages.append(
        f"Total income: Rs. {summary['total_income']:,.2f}"
    )
    messages.append(
        f"Total expenses: Rs. {summary['total_expenses']:,.2f}"
    )
    messages.append(
        f"Net balance: Rs. {summary['net_balance']:,.2f}"
    )

    if summary["net_balance"] < 0:
        messages.append(
            "Warning: Your expenses are higher than your income."
        )
    else:
        messages.append(
            "Your income is currently higher than your expenses."
        )

    if not category_data.empty:
        highest = category_data.iloc[0]
        messages.append(
            f"Highest spending category: {highest['Category']} "
            f"(Rs. {highest['Amount']:,.2f})"
        )

    if budgets is not None and not budgets.empty:
        for _, row in budgets.iterrows():
            category = row["Category"]
            budget = float(row["Budget"])

            matching = category_data[
                category_data["Category"] == category
            ]

            spent = (
                float(matching["Amount"].sum())
                if not matching.empty else 0
            )

            if spent > budget:
                messages.append(
                    f"Budget warning: {category} exceeded its budget "
                    f"by Rs. {spent - budget:,.2f}."
                )

    return messages
