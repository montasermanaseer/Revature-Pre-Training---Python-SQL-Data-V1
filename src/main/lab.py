from pathlib import Path
import sqlite3

import pandas as pd


def process_data():
    # Project paths
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "src" / "data"
    file_path = data_dir / "transactions.csv"
    database_path = data_dir / "transactions.db"

    # Step 1: Load and clean the transactions data
    # Load the tab-separated transactions.csv file into a pandas DataFrame.
    df = pd.read_csv(file_path, sep="\t")

    # Remove rows containing any missing values
    df = df.dropna()

    # Convert TransactionDate to datetime (DD-MM-YYYY -> pandas datetime)
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], format="%d-%m-%Y")

    # When storing in SQLite, use ISO format YYYY-MM-DD as TEXT
    df["TransactionDate"] = df["TransactionDate"].dt.strftime("%Y-%m-%d")

    # Step 2: Set up the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            TransactionID INTEGER PRIMARY KEY,
            CustomerID TEXT,
            Product TEXT,
            Amount REAL,
            TransactionDate TEXT,
            PaymentMethod TEXT,
            City TEXT,
            Category TEXT
        )
    """)

    # Step 3: Insert the cleaned data into SQLite
    # Replace existing data in the table with the cleaned DataFrame
    # Delete existing rows first to avoid duplicates
    cursor.execute("DELETE FROM transactions")

    insert_query = """
        INSERT INTO transactions (
            TransactionID, CustomerID, Product, Amount,
            TransactionDate, PaymentMethod, City, Category
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    records = []
    for _, row in df.iterrows():
        records.append((
            int(row["TransactionID"]),
            str(row["CustomerID"]),
            str(row["Product"]),
            float(row["Amount"]),
            str(row["TransactionDate"]),
            str(row["PaymentMethod"]),
            str(row["City"]),
            str(row["Category"]) if "Category" in row else None,
        ))

    cursor.executemany(insert_query, records)

    # Step 4: Perform SQL queries for data analysis

    # TODO: Query 1 - Top 5 Best-Selling Products
    # Find the top 5 products based on transaction count.
    print("\n--- Query 1: Top 5 Best-Selling Products ---")
    cursor.execute(
        "SELECT Product, COUNT(*) AS transaction_count FROM transactions "
        "GROUP BY Product ORDER BY transaction_count DESC LIMIT 5"
    )
    for prod, cnt in cursor.fetchall():
        print(f"{prod}: {cnt}")

    # TODO: Query 2 - Monthly Revenue Trend
    # Calculate total revenue for each month in chronological order.
    print("\n--- Query 2: Monthly Revenue Trend ---")
    cursor.execute(
        "SELECT strftime('%Y-%m', TransactionDate) AS month, "
        "ROUND(SUM(Amount),2) AS total_revenue "
        "FROM transactions GROUP BY month ORDER BY month ASC"
    )
    for month, total in cursor.fetchall():
        print(f"{month}: {total}")

    # TODO: Query 3 - Payment Method Popularity
    # Count transactions for each payment method.
    print("\n--- Query 3: Payment Method Popularity ---")
    cursor.execute(
        "SELECT PaymentMethod, COUNT(*) AS count FROM transactions "
        "GROUP BY PaymentMethod ORDER BY count DESC"
    )
    for method, cnt in cursor.fetchall():
        print(f"{method}: {cnt}")

    # TODO: Query 4 - Top 5 Cities with Most Transactions
    # Find the five cities with the highest transaction counts.
    print("\n--- Query 4: Top 5 Cities with Most Transactions ---")
    cursor.execute(
        "SELECT City, COUNT(*) AS transaction_count FROM transactions "
        "GROUP BY City ORDER BY transaction_count DESC LIMIT 5"
    )
    for city, cnt in cursor.fetchall():
        print(f"{city}: {cnt}")

    # TODO: Query 5 - Top 5 Spending Customers
    # Find the five customers with the highest total spending.
    print("\n--- Query 5: Top 5 Spending Customers ---")
    cursor.execute(
        "SELECT CustomerID, ROUND(SUM(Amount),2) AS total_spent "
        "FROM transactions GROUP BY CustomerID ORDER BY total_spent DESC LIMIT 5"
    )
    for cust, total in cursor.fetchall():
        print(f"{cust}: {total}")

    # TODO: Query 6 - Hadoop vs Spark Sales
    # Categorize products containing "Hadoop" or "Spark" and compare
    # their transaction counts and total sales.
    print("\n--- Query 6: Hadoop vs Spark Sales ---")
    cursor.execute(
        "SELECT grp AS category, COUNT(*) AS transaction_count, "
        "ROUND(SUM(Amount),2) AS total_sales FROM ("
        "SELECT *, CASE WHEN Product LIKE '%Hadoop%' THEN 'Hadoop' "
        "WHEN Product LIKE '%Spark%' THEN 'Spark' ELSE NULL END AS grp "
        "FROM transactions) WHERE grp IS NOT NULL GROUP BY grp"
    )
    for cat, cnt, total in cursor.fetchall():
        print(f"{cat} - Transactions: {cnt}, Total Sales: {total}")

    # TODO: Query 7 - Top Spending Customer per City
    # Find the customer(s) with the highest total spending in each city.
    # Use a subquery or window function. Include ties if applicable.
    print("\n--- Query 7: Top Spending Customer(s) per City ---")
    cursor.execute(
        "SELECT City, CustomerID, total_spent FROM ("
        "SELECT City, CustomerID, SUM(Amount) AS total_spent, "
        "RANK() OVER (PARTITION BY City ORDER BY SUM(Amount) DESC) AS rnk "
        "FROM transactions GROUP BY City, CustomerID) WHERE rnk = 1 ORDER BY City"
    )
    for city, cust, total in cursor.fetchall():
        print(f"{city} - {cust}: {round(total,2)}")

    # Step 5: Commit changes and close the database connection
    conn.commit()
    conn.close()
    print("\nData Processing & Advanced Analysis Completed Successfully!")


if __name__ == "__main__":
    process_data()
