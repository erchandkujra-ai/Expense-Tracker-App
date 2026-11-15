# 💰 Expense Tracker App – Personal Finance Analytics Dashboard

**Developed by: ER.CHAND KUJRA**

A Python-based Expense Tracker and Data Analytics Dashboard built using Streamlit, Pandas, NumPy, Plotly and Matplotlib. This project helps users track income, monitor expenses, analyze spending patterns and manage budgets through an interactive dashboard.

## 🚀 Project Overview

The Expense Tracker App is a beginner-friendly yet industry-oriented Data Science project designed to simplify personal financial management.

Users can add transactions, upload CSV files, visualize spending patterns, monitor category-wise budgets and identify overspending through automatic warnings.

This project uses sample or manually entered financial data. It does not connect to real bank accounts, Google Pay or PhonePe.

## ✨ Key Features

- **Financial Overview:** Total income, total expenses and net balance.
- **Transaction Management:** Add and manage income and expense records.
- **Category Analysis:** Analyze spending across different categories.
- **Monthly Trends:** Compare monthly income and expenses.
- **Payment Analysis:** Visualize spending by payment method.
- **Budget Monitoring:** Set category-wise budgets.
- **Overspending Alerts:** Receive warnings when spending approaches or exceeds a budget.
- **CSV Upload:** Import transaction data.
- **CSV Export:** Download transaction records.
- **Interactive Dashboard:** Explore financial data using Streamlit and Plotly.
- **Dark Blue Theme:** Professional dashboard interface.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |
| CSV | Data storage |

## 📁 Project Structure

```text
Expense-Tracker-App/
│
├── app.py
├── main.py
├── style.css
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── expenses.csv
│   ├── cleaned_expenses.csv
│   └── budgets.csv
│
├── notebooks/
│   └── exploratory_data_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── visualization.py
│   └── insights.py
│
├── outputs/
│   └── charts/
│
└── images/
    └── dashboard.png
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/erchandkujra-ai/Expense-Tracker-App.git
```

### 2. Open the project folder

```bash
cd Expense-Tracker-App
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Git Bash:**

```bash
source .venv/Scripts/activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser, usually at:

`http://localhost:8501`

## 📊 Dashboard Modules

1. Financial Overview
2. Add Transaction
3. Budget Manager
4. Upload / Export Data

## 📂 Dataset Format

The application expects transaction CSV files with these columns:

| Column | Description |
|---|---|
| Date | Transaction date |
| Category | Expense or income category |
| Description | Transaction details |
| Amount | Transaction amount |
| Type | Income or Expense |
| Payment_Method | Cash, UPI, Card, etc. |

Example:

```csv
Date,Category,Description,Amount,Type,Payment_Method
2026-11-01,Food,Lunch,250,Expense,UPI
2026-11-02,Salary,Monthly Salary,30000,Income,Bank Transfer
2026-11-03,Travel,Bus Ticket,100,Expense,Cash
```

## 🔮 Future Improvements

- Machine Learning-based expense prediction.
- Automatic spending pattern detection.
- PDF financial report generation.
- User authentication and profiles.
- Database integration.
- Mobile-friendly dashboard.
- Advanced financial recommendations.

## 🎯 Project Objectives

- Apply Python programming to a practical problem.
- Learn data cleaning and data analysis.
- Build interactive dashboards.
- Understand financial data visualization.
- Develop a GitHub-ready Data Science portfolio project.

## 👨‍💻 Author

**ER.CHAND KUJRA**

- GitHub: [@erchandkujra-ai](https://github.com/erchandkujra-ai)
- Project: [Expense Tracker App](https://github.com/erchandkujra-ai/Expense-Tracker-App)

## 📜 License

This project is intended for educational and portfolio purposes. See the `LICENSE` file for licensing details.

---

⭐ If you find this project useful, consider giving it a star on GitHub.

**Built with Python, Data Science and Streamlit.**