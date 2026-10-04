# Big Data Assignment

## Project Overview

In this project, you will work with a dataset of transactions from a business or e-commerce platform. Your task is to process and clean the data using Python and pandas, store the cleaned data in a SQLite database, and use SQL queries to derive meaningful business insights.

The project covers:

- Loading and cleaning transaction data with pandas
- Converting date values into an appropriate format
- Creating and populating a SQLite database
- Writing SQL queries for business analysis
- Using SQL aggregation, filtering, subqueries, and window functions
- Validating query results
- Reporting your final results through console output

## Getting Started

1. Open the provided assignment project in VS Code.
2. Open `src/main/lab.py`.
3. Complete the TODO sections in `lab.py`.
4. The dataset is provided in `src/data/transactions.csv`.
5. Run the application and verify that all required query results are displayed in the console.

> **Important:** The provided file is named `transactions.csv`, but its values are separated by tab characters. Make sure you load it accordingly.

---

## Step 1: Data Cleaning

### Load the Data

Load the provided `transactions.csv` dataset into a pandas DataFrame.

### Handle Missing Values

Inspect the dataset for missing or null values. Remove any rows that contain missing values so that the data used for analysis is complete.

### Convert Data Types

The `TransactionDate` column contains dates in `DD-MM-YYYY` format. Convert this column to a proper pandas datetime type using the correct date format.

When storing the data in SQLite, the date may be stored as `TEXT` in a consistent date representation.

---

## Step 2: Create the SQLite Database and Table

Using Python's built-in `sqlite3` module, create or connect to the SQLite database located in `src/data/transactions.db`.

Create a table named `transactions` with the following schema:

| Column | SQLite Type | Constraint |
|---|---|---|
| `TransactionID` | `INTEGER` | Primary Key |
| `CustomerID` | `TEXT` | — |
| `Product` | `TEXT` | — |
| `Amount` | `REAL` | — |
| `TransactionDate` | `TEXT` | — |
| `PaymentMethod` | `TEXT` | — |
| `City` | `TEXT` | — |
| `Category` | `TEXT` | — |

---

## Step 3: Insert Data into SQLite

Insert the cleaned pandas DataFrame into the `transactions` table.

If the table already contains data from an earlier run, replace the existing data with the newly cleaned data. Do not create duplicate records when the program is run multiple times.

---

## Step 4: Perform SQL Queries for Data Analysis

Write SQL queries to answer the following business questions.

### Query 1: Top 5 Best-Selling Products

Identify the top 5 products based on the total number of transactions (sales count).

Return the product name and its transaction count, ordered from highest to lowest.

### Query 2: Monthly Revenue Trend

Calculate the total revenue for each month by summing `Amount`.

Display the results in chronological order.

### Query 3: Payment Method Popularity

Determine the popularity of each payment method by counting the number of transactions made using each method.

Order the results from most-used to least-used payment method.

### Query 4: Top 5 Cities with Most Transactions

Identify the top 5 cities with the highest number of transactions.

Return the city and transaction count, ordered from highest to lowest.

### Query 5: Top 5 Spending Customers

Identify the top 5 customers who have spent the most.

Calculate the total amount spent by each customer and order the results by total spending in descending order.

### Query 6: Hadoop vs Spark Sales

Identify products whose names contain `Hadoop` or `Spark`.

Categorize each matching product into either the `Hadoop` or `Spark` group and compare the two groups using:

- Transaction count
- Total sales/revenue

Only products containing `Hadoop` or `Spark` should be included in this comparison.

### Query 7: Top Spending Customer per City

Find the customer with the highest total spending within each city.

Use either a subquery or a SQL window function such as `RANK()` or `DENSE_RANK()`.

If multiple customers are tied for the highest spending in a city, include all customers tied for first place.

---

## Step 5: Execute and Verify Your Queries

Execute all seven SQL queries against the SQLite database.

For each query:

- Display the results in the console.
- Verify that the results are reasonable based on the dataset.
- Check that the ordering and aggregation are correct.
- If a result is unexpected, review and debug your SQL query.

Make sure the final console output clearly identifies each analysis section.

---

## Step 6: Clean Up

After all queries have been executed:

1. Commit any database changes.
2. Close the SQLite database connection properly.
3. Confirm that the program terminates without errors.

---

## Project Submission Guidelines

1. Run the completed program successfully.
2. Take a screenshot showing the final console output containing the results of the required analyses.
3. Add the screenshot to your lab folder.
4. Compress the entire lab folder into a ZIP file.
5. Remove the `.venv` directory before creating the ZIP file, if one was created during development.
6. Submit the ZIP file according to the assignment submission process.
