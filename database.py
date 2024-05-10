import psycopg2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


# Initialize Firebase with your credentials file
def initialize_firebase():
    cred = credentials.Certificate("serviceAccountKey.json")  # Path to your service account key JSON file
    firebase_admin.initialize_app(cred)
    db_firestore = firestore.client()


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

# Function to insert donor data into the PostgreSQL database and Firebase Realtime Database
def insert_donor(donor_id, name, contact, blood_type, date_of_birth, gender, health_history, last_donation_date):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            insert_query = """INSERT INTO donors(donor_id, name, contact, blood_type, date_of_birth, gender, health_history, last_donation_date)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (
            donor_id, name, contact, blood_type, date_of_birth, gender, health_history, last_donation_date))
            db.commit()
            print("Donor's data inserted successfully into PostgreSQL!")

            # Insert data into Firebase
            insert_donor_firebase(donor_id, name, contact, blood_type, date_of_birth, gender, health_history,
                                  last_donation_date)
        except psycopg2.Error as e:
            print("Error inserting donor data into PostgreSQL:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()


# Function to insert donor data into Firebase Realtime Database
def insert_donor_firebase(donor_id, name, contact, blood_type, date_of_birth, gender, health_history,
                          last_donation_date):
    ref = db.reference('donors')  # Reference to the 'donors' node in your Firebase database
    ref.child(donor_id).set({
        'name': name,
        'contact': contact,
        'blood_type': blood_type,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'health_history': health_history,
        'last_donation_date': last_donation_date
    })


# Function to recieve donor data into the database
def insert_receiver(recipient_id, name, contact, blood_type, date_of_birth, gender, health_condition, hospital):
    # Insert into PostgreSQL
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            insert_query = """INSERT INTO recipients(recipient_id, name, contact, blood_type, date_of_birth, gender, health_condition, hospital)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query,
                           (recipient_id, name, contact, blood_type, date_of_birth, gender, health_condition, hospital))
            db.commit()
            print("Receiver's data inserted successfully into PostgreSQL!")

            # Insert data into Firebase
            insert_receiver_firebase(recipient_id, name, contact, blood_type, date_of_birth, gender, health_condition,
                                     hospital)

        except psycopg2.Error as e:
            print("Error inserting recipient data into PostgreSQL:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def insert_blood_bank(blood_bank_id, name, location, contact, services_provided, operating_hours):
    # Insert into PostgreSQL
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            insert_query = """INSERT INTO blood_banks(blood_bank_id, name, location, contact, services_provided, operating_hours)
                              VALUES(%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (blood_bank_id, name, location, contact, services_provided, operating_hours))
            db.commit()
            print("Blood bank inserted successfully into PostgreSQL!")
            
            # Insert data into Firebase
            insert_blood_bank_firebase(blood_bank_id, name, location, contact, services_provided, operating_hours)
            
        except psycopg2.Error as e:
            print("Error inserting data into PostgreSQL:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def insert_blood_bank_firebase(blood_bank_id, name, location, contact, services_provided, operating_hours):
    ref = db.reference('blood_banks')  # Reference to the 'blood_banks' node in your Firebase database
    ref.child(blood_bank_id).set({
        'name': name,
        'location': location,
        'contact': contact,
        'services_provided': services_provided,
        'operating_hours': operating_hours
    })



def insert_donations(donor_id, blood_bank_id, quantity_donated, blood_type, health_check_information):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
           
            trigger_query_before = """
                CREATE OR REPLACE FUNCTION before_insert_donations_trigger()
                RETURNS TRIGGER AS $$
                BEGIN
                    -- Update the donor's last donation date
                    UPDATE donors
                    SET last_donation_date = CURRENT_DATE
                    WHERE donor_id = NEW.donor_id;

                    -- Validate the quantity of blood donated
                    IF NEW.quantity_donated > 500 THEN
                        RAISE EXCEPTION 'Quantity of blood donated exceeds safe limits';
                    END IF;

                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                
                CREATE OR REPLACE TRIGGER donations_before_insert_trigger
                BEFORE INSERT ON donations
                FOR EACH ROW
                EXECUTE FUNCTION before_insert_donations_trigger();
            """
            cursor.execute(trigger_query_before)
            db.commit()

            # trigger_query_after = """
            #     CREATE OR REPLACE FUNCTION after_insert_donations_trigger()
            #     RETURNS TRIGGER AS $$
            #     BEGIN
            #         -- Update blood inventory to reflect the new donation
            #         UPDATE blood_inventory

            #         -- Check if the quantity of a particular blood type falls below a certain threshold
            #         IF (SELECT quantity_available FROM blood_inventory WHERE blood_bank_id = NEW.blood_bank_id AND blood_type = NEW.blood_type) < 200 THEN
            #             -- Notify blood bank administrator (Replace 'notify_administrator()' with your notification logic)
            #             PERFORM notify_administrator('Blood inventory for blood type ' || NEW.blood_type || ' fell below threshold at blood bank ' || NEW.blood_bank_id);
            #         END IF;

            #         RETURN NEW;
            #     END;
            #     $$ LANGUAGE plpgsql;

            #     -- Create the trigger
            #     CREATE OR REPLACE TRIGGER donations_after_insert_trigger
            #     AFTER INSERT ON donations
            #     FOR EACH ROW
            #     EXECUTE FUNCTION after_insert_donations_trigger();
            #     """
            
            # cursor.execute(trigger_query_after)
            # db.commit()

            trigger_query_after1 = """
                CREATE OR REPLACE FUNCTION update_inventory()
                RETURNS TRIGGER AS $$
                
                BEGIN
                    UPDATE blood_inventory
                    SET expiry_date = NEW.donation_date + INTERVAL '30 days',
                        quantity_available = COALESCE(quantity_available, 0) + NEW.quantity_donated,
                        blood_type = NEW.blood_type
                    WHERE donor_id = NEW.donor_id;

                    RETURN NEW;
                
                END;

                $$ LANGUAGE plpgsql;

                CREATE OR REPLACE TRIGGER update_blood_inventory
                AFTER INSERT ON donations
                FOR EACH ROW
                EXECUTE FUNCTION update_inventory();   
            """

            cursor.execute(trigger_query_after1)
            db.commit()
            insert_query = """INSERT INTO donations(donor_id, blood_bank_id, quantity_donated, blood_type, health_check_information, donation_date)
                              VALUES(%s, %s, %s, %s, %s, CURRENT_DATE)"""
            cursor.execute(insert_query, (donor_id, blood_bank_id, quantity_donated, blood_type, health_check_information))
            db.commit()

            print("Data inserted successfully!")
            
        except psycopg2.Error as e:
            print("Error creating trigger:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def insert_blood_inventory(inventory_id, blood_bank_id, donor_id):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()

            trigger_query = """
                CREATE OR REPLACE FUNCTION blood_threshold()
                RETURNS TRIGGER AS $$
                DECLARE
                    blood_type_threshold INT := 100;  
                BEGIN
                    -- if the quantity of any blood type falls below the threshold
                    IF NEW.quantity_available < blood_type_threshold THEN
                       
                        RAISE NOTICE 'Alert: Quantity of blood type % is below threshold', NEW.blood_type;
                    END IF;

                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                
                CREATE OR REPLACE TRIGGER blood_inventory_after_update_trigger
                AFTER UPDATE ON blood_inventory
                FOR EACH ROW
                EXECUTE FUNCTION blood_threshold();
            """
            cursor.execute(trigger_query)
            db.commit()
            insert_query = """INSERT INTO blood_inventory(inventory_id, blood_bank_id, donor_id)
                              VALUES(%s, %s, %s)"""
            cursor.execute(insert_query, (inventory_id, blood_bank_id, donor_id))
            db.commit()
            print("Data inserted successfully!")
        except psycopg2.Error as e:
            print("Error inserting data:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def before_insert_blood_inventory():
    try:
        db = get_db_connection()
        if db:
            cursor = db.cursor()
            trigger_query = """
                CREATE OR REPLACE FUNCTION before_insert_blood_inventory()
                RETURNS TRIGGER AS $$
                DECLARE
                    blood_bank_exists BOOLEAN;
                BEGIN
                    -- Check if the blood bank ID exists in the blood bank table
                    SELECT EXISTS(SELECT 1 FROM blood_bank WHERE blood_bank_id = NEW.blood_bank_id) INTO blood_bank_exists;
                    IF NOT blood_bank_exists THEN
                        RAISE EXCEPTION 'Blood bank with ID % does not exist', NEW.blood_bank_id;
                    END IF;
                    
                   -- Ensure that the expiry date is not in the past
                    IF NEW.expiry_date < CURRENT_DATE THEN
                        RAISE EXCEPTION 'Past Expiry date';
                    END IF;

                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                
                CREATE OR REPLACE TRIGGER blood_inventory_before_insert_trigger
                BEFORE INSERT ON blood_inventory
                FOR EACH ROW
                EXECUTE FUNCTION before_insert_blood_inventory();
            """
            cursor.execute(trigger_query)
            db.commit()
            cursor.close()
    except psycopg2.Error as e:
        print("Error creating trigger:", e)
        if db:
            db.rollback()
    finally:
        if db:
            db.close()


def view_donation(donor_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM donations WHERE donor_id = %s", (donor_id,))
        donation_records = cursor.fetchall()
        if donation_records:
            for record in donation_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found for donor ID:", donor_id)
    except psycopg2.Error as e:
        print("Error viewing donor records:", e)
    finally:
        cursor.close()
        db.close()
        return donation_records
    
def view_receiver(recipient_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM recipients WHERE recipient_id = %s", (recipient_id))
        receiver_records = cursor.fetchall()
        if receiver_records:
            for record in receiver_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found for receiver ID:", recipient_id)
    except psycopg2.Error as e:
        print("Error viewing receiver records:", e)
    finally:
        cursor.close()
        db.close()
        return receiver_records
    
def view_bank(blood_bank_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM blood_banks WHERE blood_bank_id = %s", (blood_bank_id))
        bank_records = cursor.fetchall()
        if bank_records:
            for record in bank_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found for Blood Bank ID:", blood_bank_id)
    except psycopg2.Error as e:
        print("Error viewing blood bank records:", e)
    finally:
        cursor.close()
        db.close()
        return bank_records
    
def view_all_inventory():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM blood_inventory")
        inventory_records = cursor.fetchall()
        if inventory_records:
            for record in inventory_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found:")
    except psycopg2.Error as e:
        print("Error viewing Inventory records:", e)
    finally:
        cursor.close()
        db.close()
        return inventory_records
    
def view_all_banks():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM blood_banks")
        bank_records = cursor.fetchall()
        if bank_records:
            for record in bank_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found:")
    except psycopg2.Error as e:
        print("Error viewing Bank records:", e)
    finally:
        cursor.close()
        db.close()
        return bank_records
    
def view_inventory(blood_type):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT blood_bank_id, SUM(quantity_available) AS total_quantity_available FROM blood_inventory 
                        WHERE blood_type = %s 
                        GROUP BY blood_bank_id""", (blood_type,))
        inventory_records = cursor.fetchall()
        if inventory_records:
            for record in inventory_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found for blood_type:", blood_type)
    except psycopg2.Error as e:
        print("Error viewing Inventory records:", e)
    finally:
        cursor.close()
        db.close()
        return inventory_records


def view_donor(donor_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM donors WHERE donor_id = %s", (donor_id))
        donor_records = cursor.fetchall()
        if donor_records:
            for record in donor_records:
                print(record)  # Or process the records as needed
        else:
            print("No records found for donor ID:", donor_id)
    except psycopg2.Error as e:
        print("Error viewing donor records:", e)
    finally:
        cursor.close()
        db.close()
        return donor_records

def delete_donor(donor_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM donors WHERE donor_id = %s", (donor_id,))
        db.commit()  # Don't forget to commit the transaction
    except Exception as e:
        print("Error deleting donor:", e)
    finally:
        cursor.close()
        db.close()

def delete_receiver(recipient_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM recipients WHERE recipient_id = %s", (recipient_id,))
        db.commit()  # Don't forget to commit the transaction
    except Exception as e:
        print("Error deleting recipient:", e)
    finally:
        cursor.close()
        db.close()

def delete_bank(blood_bank_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM blood_banks WHERE blood_bank_id = %s", (blood_bank_id,))
        db.commit()  # Don't forget to commit the transaction
    except Exception as e:
        print("Error deleting bank:", e)
    finally:
        cursor.close()
        db.close()
        
