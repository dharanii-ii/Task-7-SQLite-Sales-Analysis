# Task 7: SQLite Sales Analysis Using Python

## Objective

The objective of this task is to connect Python with a SQLite database, run basic SQL queries, summarize sales data, and visualize the results using charts.

## Tools Used

- Python
- SQLite
- pandas
- matplotlib

## Dataset Description

The project uses a small sales dataset stored in a SQLite database named `sales_data.db`.

Table name: `sales`

| Column | Description |
| --- | --- |
| id | Unique sale ID |
| product | Product name |
| quantity | Number of units sold |
| price | Product price |
| sale_date | Date of sale |

## SQL Queries Used

Product-wise quantity and revenue:

```sql
SELECT
    product,
    SUM(quantity) AS Total_Quantity,
    SUM(quantity * price) AS Revenue
FROM sales
GROUP BY product
ORDER BY Revenue DESC;
```

Overall sales summary:

```sql
SELECT
    COUNT(*) AS Total_Orders,
    SUM(quantity) AS Total_Items_Sold,
    SUM(quantity * price) AS Total_Revenue,
    AVG(price) AS Average_Product_Price
FROM sales;
```

Highest revenue product:

```sql
SELECT
    product,
    SUM(quantity * price) AS Revenue
FROM sales
GROUP BY product
ORDER BY Revenue DESC
LIMIT 1;
```

Best selling product:

```sql
SELECT
    product,
    SUM(quantity) AS Quantity
FROM sales
GROUP BY product
ORDER BY Quantity DESC
LIMIT 1;
```

## Charts Generated

- `Revenue_BarChart.png`
- `Quantity_BarChart.png`
- `Revenue_PieChart.png`

## Key Insights

- Laptop generated the highest revenue.
- Mouse was the best selling product by quantity.
- Total revenue from all sales was Rs. 471,400.
- Laptops contributed the largest percentage of total revenue.

## How to Run

Install the required Python packages if needed:

```bash
pip install pandas matplotlib
```

Run the project:

```bash
python task7.py
```

The script creates `sales_data.db`, prints the sales summary, and saves all chart images in the same folder.

