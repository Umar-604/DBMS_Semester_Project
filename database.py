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

# Function to recieve donor data into the database
def insert_receiver():
    recipent_id=input("Enter recipent ID:")
    name =input("Enter name:")
    contact=input("Enter contact number:")
    blood_type=input("Enter blood type:")
    date_of_birth=input("Enter date of birth(YYYY-MM-DD):")
    gender=input("Enter gender:")
    health_history=input("Enter health history:")
    hospital=input("Enter hospitals name:")
    db=get_db_connection()
    if db:
        try:
            cursor =db.cursor()
            insert_query="""INSERT INTO donors(recipient_id, name, contact, blood_type, date_of_birth, gender, health_history, hospital)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (recipent_id, name, contact, blood_type, date_of_birth, gender, health_history, hospital))
            db.commit()
            print("Receiver's data inserted successfully!")
        except psycopg2.Error as e:
            print("Error inserting donor data:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def view_donor_data(table_name):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()
    db.close()
    return rows
table_name = input("Enter table name : ")
data = view_donor_data(table_name)
for row in data:
    print(row) 
def after_update_blood_inventory():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
           
            trigger_query = """
                CREATE OR REPLACE FUNCTION after_update_blood_inventory()
                RETURNS TRIGGER AS $$
                DECLARE
                    blood_type_threshold INT := 100;  
                    blood_expiry_period INTERVAL := '90 days'; 
                BEGIN
                    -- Send alerts if the quantity of any blood type falls below the threshold
                    IF NEW.quantity < blood_type_threshold THEN
                    
                        RAISE NOTICE 'Alert: Quantity of blood type % is below threshold', NEW.blood_type;
                    END IF;

                    -- Update the expiry date of blood units based on their lifespan
                    UPDATE blood_inventory
                    SET expiry_date = NEW.date_collected + blood_expiry_period
                    WHERE blood_id = NEW.blood_id;

                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                
                CREATE TRIGGER blood_inventory_after_update_trigger
                AFTER UPDATE ON blood_inventory
                FOR EACH ROW
                EXECUTE FUNCTION after_update_blood_inventory();
            """
            cursor.execute(trigger_query)
            db.commit()
            
        except psycopg2.Error as e:
            print("Error creating trigger:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()
           
# Call the insert_donor function
insert_donor()
insert_receiver()


