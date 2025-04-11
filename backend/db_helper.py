import os
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "expense_manager")
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_a_given_date(expense_date):
    logger.info(f"fetch_expenses_for_a_given_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM  expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date:{expense_date}, amount:{amount}, category:{category}, notes:{notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES(%s, %s, %s, %s)",
            (expense_date, amount, category, notes)

        )


def delete_expenses_for_a_given_date(expense_date):
    logger.info(f"delete_expenses_for_a_given_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start_date:{start_date}, end_date:{end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, sum(amount)  as total 
            FROM  expenses 
            WHERE expense_date 
            BETWEEN  %s and %s 
            GROUP BY  category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


def get_expenses_by_month():
    logger.info("fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT MONTH(expense_date) AS expense_month, 
                      MONTHNAME(expense_date) AS month_name,
                      SUM(amount) AS total 
               FROM expenses
               GROUP BY expense_month, month_name
               ORDER BY expense_month;
            '''
        )
        return cursor.fetchall()

# def get_expenses_by_month():
#     logger.info(f"fetch_expense_summary_by_months")
#     with get_db_cursor() as cursor:
#         cursor.execute(
#             '''SELECT month(expense_date) as expense_month,
#                monthname(expense_date) as month_name,
#                sum(amount) as total FROM expenses
#                GROUP BY expense_month, month_name;
#             '''
#         )
#         data = cursor.fetchall()
#         return data


if __name__ == "__main__":
    '''****Fetching Expenses for Date: 2024-08-07 ******'''
    # expenses_on_7aug = fetch_expenses_for_a_given_date("2024-08-07")
    # print(expenses_on_7aug)

    '''****Inserting a New Expenses: ******'''
    # insert_expense("2025-04-06", 900, "Food", "Buy foods to feed stomach")
    # if insert_expense:
    #     print("Insertion successful")

    '''****Deleting an Expense for a Given Date:2025-04-06 ******'''
    # delete_expenses_for_a_given_date("2025-04-06")
    # if delete_expenses_for_a_given_date:
    #     print("Deletion successful")

    '''****Total Expenses Per Category for a Given Date range: "2024-08-01", and "2024-08-25" ******'''
    # summary = fetch_expense_summary("2024-08-01", "2024-08-25")
    # for expense in summary:
    #     print(expense)
