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

        self.table_name = "RawGoogleFlights"

    def create_table(self):
        # Query to check if the table already exists
        check_table_query = f"""
        SELECT COUNT(*) 
        FROM sysobjects 
        WHERE name='{self.table_name}' AND xtype='U'
        """

        # Execute the check
        self.cursor.execute(check_table_query)
        result = self.cursor.fetchone()

        if result[0] > 0:
            print(f"Table {self.table_name} already exists.")
        else:
            create_table_query = f"""
            CREATE TABLE {self.table_name} (
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
            print(f"Successfully created table {self.table_name}.")

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

        insert_query = f"""
        INSERT INTO {self.table_name} (duration, stops, price, departure_landing, stopping_locations, company, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
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
        except pyodbc.Error as e:
            print(f"Error inserting data: {e}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def test_connection(self):
        try:
            self.cursor.execute("SELECT GETDATE()")
            result = self.cursor.fetchone()
            print(f"Connection successful. Server date/time: {result[0]}")
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")


# Example usage to test the connection
if __name__ == "__main__":
    db = DBHandler()
    db.test_connection()
    db.create_table()
    db.close_connection()
