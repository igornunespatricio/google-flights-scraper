import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DBHandler:
    def __init__(self):
        # Initialize the connection to SQL Server using environment variables
        self.conn = pyodbc.connect(
            f"DRIVER={os.getenv('DB_DRIVER')};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_DATABASE')};"
            f"UID={os.getenv('DB_USERNAME')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
        )
        self.cursor = self.conn.cursor()

    # Create the flights table if it doesn't already exist

    def create_table(self):
        table_name = "googleFlights"

        # Query to check if the table already exists
        check_table_query = f"""
        SELECT COUNT(*) 
        FROM sysobjects 
        WHERE name='{table_name}' AND xtype='U'
        """

        # Execute the check
        self.cursor.execute(check_table_query)
        result = self.cursor.fetchone()

        if result[0] > 0:
            # Table exists, print a message
            print(f"Table {table_name} already exists.")
        else:
            # Table does not exist, create it
            create_table_query = f"""
            CREATE TABLE {table_name} (
                id INT IDENTITY(1,1) PRIMARY KEY,
                duration NVARCHAR(50),             
                stops NVARCHAR(50),                
                price NVARCHAR(50),                
                departure_landing NVARCHAR(50),   
                stopping_locations NVARCHAR(50),  
                company NVARCHAR(50),              
                scraped_at DATETIME
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Successfully created table {table_name}.")

    # Insert data into the flights table
    def insert_data(
        self,
        duration,
        stops,
        price,
        departure_landing,
        stopping_locations,
        company,
        scraped_at,
    ):
        duration_str = ",".join(duration) if duration else None
        stops_str = ",".join(stops) if stops else None
        price_str = ",".join(price) if price else None
        stopping_locations_str = (
            ",".join(stopping_locations) if stopping_locations else None
        )

        insert_query = """
        INSERT INTO flights (duration, stops, price, departure_landing, stopping_locations, company, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(
            insert_query,
            (
                duration_str,
                stops_str,
                price_str,
                departure_landing,
                stopping_locations_str,
                company,
                scraped_at,
            ),
        )
        self.conn.commit()

    # Close the connection when done
    def close_connection(self):
        self.conn.close()

    # Test connection to the database
    def test_connection(self):
        try:
            # Test with a simple query (e.g., get current server date)
            self.cursor.execute("SELECT GETDATE()")
            result = self.cursor.fetchone()
            print(f"Connection successful. Server date/time: {result[0]}")
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")


# Example usage to test the connection
if __name__ == "__main__":
    db = DBHandler()
    db.create_table()
    db.close_connection()
