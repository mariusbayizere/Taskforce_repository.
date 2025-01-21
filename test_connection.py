import psycopg2

try:
    conn = psycopg2.connect(
        dbname="wallet_app_0qy4",
        user="root",
        password="your_password",
        host="dpg-cu79rdrtq21c739l0ehg-a",
        #port=5432
    )
    print("Connection successful!")
except psycopg2.OperationalError as e:
    print("Database connection failed!")
    print(f"Error: {e}")

