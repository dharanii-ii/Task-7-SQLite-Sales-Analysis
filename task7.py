import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sales_data.db"


SALES_DATA = [
    (1, "Laptop", 2, 55000.0, "2026-06-01"),
    (2, "Mouse", 8, 500.0, "2026-06-01"),
    (3, "Keyboard", 5, 1200.0, "2026-06-02"),
    (4, "Laptop", 1, 55000.0, "2026-06-03"),
    (5, "Mouse", 10, 500.0, "2026-06-03"),
    (6, "Monitor", 3, 12000.0, "2026-06-04"),
    (7, "Keyboard", 7, 1200.0, "2026-06-05"),
    (8, "Monitor", 2, 12000.0, "2026-06-05"),
    (9, "Laptop", 4, 55000.0, "2026-06-06"),
    (10, "Mouse", 6, 500.0, "2026-06-07"),
]


def format_currency(value):
    return f"Rs. {value:,.0f}"


def create_database(conn):
    conn.execute("DROP TABLE IF EXISTS sales")
    conn.execute(
        """
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            sale_date TEXT NOT NULL
        )
        """
    )
    conn.executemany(
        """
        INSERT INTO sales (id, product, quantity, price, sale_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        SALES_DATA,
    )
    conn.commit()


def save_revenue_chart(df):
    plt.figure(figsize=(8, 5))
    plt.barh(df["product"], df["Revenue"], color="#3d6fb6")
    plt.title("Revenue by Product")
    plt.xlabel("Revenue (Rs.)")
    plt.ylabel("Product")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(BASE_DIR / "Revenue_BarChart.png", dpi=150)
    plt.close()


def save_quantity_chart(df):
    plt.figure(figsize=(8, 5))
    plt.bar(df["product"], df["Total_Quantity"], color="#2f9c7c")
    plt.title("Quantity Sold by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Quantity Sold")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "Quantity_BarChart.png", dpi=150)
    plt.close()


def save_revenue_pie_chart(df):
    plt.figure(figsize=(7, 7))
    plt.pie(
        df["Revenue"],
        labels=df["product"],
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Revenue Share by Product")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "Revenue_PieChart.png", dpi=150)
    plt.close()


def main():
    with sqlite3.connect(DB_PATH) as conn:
        create_database(conn)

        product_query = """
        SELECT
            product,
            SUM(quantity) AS Total_Quantity,
            SUM(quantity * price) AS Revenue
        FROM sales
        GROUP BY product
        ORDER BY Revenue DESC;
        """
        df = pd.read_sql_query(product_query, conn)
        df["Revenue_Percentage"] = round(df["Revenue"] / df["Revenue"].sum() * 100, 2)

        summary_query = """
        SELECT
            COUNT(*) AS Total_Orders,
            SUM(quantity) AS Total_Items_Sold,
            SUM(quantity * price) AS Total_Revenue,
            AVG(price) AS Average_Product_Price
        FROM sales;
        """
        summary = pd.read_sql_query(summary_query, conn).iloc[0]

        highest_revenue_query = """
        SELECT
            product,
            SUM(quantity * price) AS Revenue
        FROM sales
        GROUP BY product
        ORDER BY Revenue DESC
        LIMIT 1;
        """
        highest_revenue = pd.read_sql_query(highest_revenue_query, conn).iloc[0]

        best_selling_query = """
        SELECT
            product,
            SUM(quantity) AS Quantity
        FROM sales
        GROUP BY product
        ORDER BY Quantity DESC
        LIMIT 1;
        """
        best_selling = pd.read_sql_query(best_selling_query, conn).iloc[0]

    print("=" * 40)
    print("SALES SUMMARY")
    print("=" * 40)
    print(f"Total Orders            : {int(summary['Total_Orders'])}")
    print(f"Total Quantity Sold     : {int(summary['Total_Items_Sold'])}")
    print(f"Total Revenue           : {format_currency(summary['Total_Revenue'])}")
    print(f"Highest Revenue Product : {highest_revenue['product']}")
    print(f"Highest Product Revenue : {format_currency(highest_revenue['Revenue'])}")
    print(f"Best Selling Product    : {best_selling['product']}")
    print(f"Best Selling Quantity   : {int(best_selling['Quantity'])}")
    print(f"Average Product Price   : {format_currency(summary['Average_Product_Price'])}")
    print("=" * 40)
    print()

    print("PRODUCT-WISE SALES ANALYSIS")
    print(df.to_string(index=False))

    save_revenue_chart(df)
    save_quantity_chart(df)
    save_revenue_pie_chart(df)

    print()
    print("Charts saved:")
    print("- Revenue_BarChart.png")
    print("- Quantity_BarChart.png")
    print("- Revenue_PieChart.png")


if __name__ == "__main__":
    main()
