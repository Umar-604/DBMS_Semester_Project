import psycopg2

# Function to establish a connection to the database
def get_db_connection():
    try:
        return psycopg2.connect(
            dbname="Blood Donation",
            user="postgres",
            password="pgadmin4",
            host="localhost"
        )
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        return None

# Function to insert donor data into the database
def insert_donor():
    # Get donor data from the user
    donor_id = input("Enter donor ID: ")
    name = input("Enter name: ")
    contact = input("Enter contact number: ")
    blood_type = input("Enter blood type: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
    gender = input("Enter gender: ")
    health_history = input("Enter health history: ")
    last_donation_date = input("Enter last donation date (YYYY-MM-DD): ")

# Call the insert_donor function
insert_donor()