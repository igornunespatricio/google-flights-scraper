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
                duration NVARCHAR(150),
                number_stops NVARCHAR(150),
                price NVARCHAR(150),
                departure_landing_airports NVARCHAR(150),
                departure_landing_cities NVARCHAR(150),
                stopping_locations NVARCHAR(150),
                company NVARCHAR(150),
                ticket_type NVARCHAR(150),
                number_passengers NVARCHAR(150),
                flight_class NVARCHAR(150),
                departure_date DATE,
                return_date DATE,
                departure_landing_times NVARCHAR(150),
                scraped_at DATETIME
            )
        """

            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Successfully created table {self.table_name}.")

    def insert_data(
        self,
        duration,
        number_stops,
        price,
        departure_landing_airports,
        departure_landing_cities,
        stopping_locations,
        company,
        ticket_type,
        number_passengers,
        flight_class,
        departure_date,
        return_date,
        departure_landing_times,
        scraped_at,
    ):
        insert_query = f"""
        INSERT INTO {self.table_name} (
            duration, number_stops, price, departure_landing_airports, 
            departure_landing_cities, stopping_locations, company, 
            ticket_type, number_passengers, flight_class, departure_date, 
            return_date, departure_landing_times, scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(
                insert_query,
                (
                    duration,
                    number_stops,
                    price,
                    departure_landing_airports,
                    departure_landing_cities,
                    stopping_locations,
                    company,
                    ticket_type,
                    number_passengers,
                    flight_class,
                    departure_date,
                    return_date,
                    departure_landing_times,
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
