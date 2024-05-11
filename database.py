import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db as firebase_db
from datetime import timedelta


# Initialize Firebase with your credentials file
cred = credentials.Certificate('serviceAccountKey.json')

try:
    firebase_admin.initialize_app(cred)
    db = firestore.client()  # Initialize Firestore client
except ValueError:
    # If Firebase Admin SDK is already initialized, retrieve the default app
    pass


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
    try:
        collection_ref = db.collection('donors')  # Reference to the 'donors' node in your Firebase database
        new_doc_ref = collection_ref.add({
            'donor_id': donor_id,
            'name': name,
            'contact': contact,
            'blood_type': blood_type,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'health_history': health_history,
            'last_donation_date': last_donation_date
        })
        print("Donor's data inserted successfully with ID:", donor_id)
    except Exception as e:
        print("Error inserting donor data:", e)


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
            insert_receiver_firebase(recipient_id, name, contact, blood_type, date_of_birth, gender, health_condition, hospital)
            
        except psycopg2.Error as e:
            print("Error inserting recipient data into PostgreSQL:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def insert_receiver_firebase(recipient_id, name, contact, blood_type, date_of_birth, gender, health_condition,
                          hospital):
    try:
        collection_ref = db.collection('receivers')  # Reference to the 'donors' node in your Firebase database
        new_doc_ref = collection_ref.add({
            'recipient_id': recipient_id,
            'name': name,
            'contact': contact,
            'blood_type': blood_type,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'health_condition': health_condition,
            'hospital': hospital
        })
        print("Receiver's data inserted successfully with ID:", recipient_id)
    except Exception as e:
        print("Error inserting receiver data:", e)



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
    try:
        collection_ref = db.collection('blood_banks')  # Reference to the 'donors' node in your Firebase database
        new_doc_ref = collection_ref.add({

        'blood_bank_id': blood_bank_id,
        'name': name,
        'location': location,
        'contact': contact,
        'services_provided': services_provided,
        'operating_hours': operating_hours

        })
        print("Blood Bank data inserted successfully with ID:", blood_bank_id)
    except Exception as e:
        print("Error inserting Blood Bank data:", e)

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

            # Insert data into Firebase
            insert_donation_firebase(donor_id, blood_bank_id, quantity_donated, blood_type, health_check_information)
            update_blood_inventory_firebase(blood_bank_id, quantity_donated, blood_type, donor_id)

def insert_donation_firebase(donor_id, blood_bank_id, quantity_donated, blood_type, health_check_information):
    try:
        collection_ref = db.collection('Donations')  # Reference to the 'donors' node in your Firebase database
        new_doc_ref = collection_ref.add({

        'donor_id': donor_id,
        'blood_bank_id': blood_bank_id,
        'quantity_donated': quantity_donated,
        'blood_type': blood_type,
        'health_check_information': health_check_information

        })
        print("Donation data inserted successfully")
    except Exception as e:
        print("Error inserting Blood Bank data:", e)

def update_blood_inventory_firebase(blood_bank_id, quantity_donated, blood_type, donor_id):
    try:
        # Calculate expiry date (30 days from donation date)

        collection_ref = db.collection('blood_inventory')  # Reference to the 'blood_inventory' collection in your Firebase database
        new_doc_ref = collection_ref.add({
            'blood_bank_id': blood_bank_id,
            'blood_type': blood_type,
            'quantity_donated': quantity_donated,
            'donor_id': donor_id,
        })
        print("Blood inventory Updated successfully")
    except Exception as e:
        print("Error updating Blood inventory data:", e)


def insert_blood_inventory(inventory_id, blood_bank_id, donor_id):
    # Connect to PostgreSQL
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()

            # Create trigger for checking blood quantity threshold
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

            # Insert data into the blood_inventory table
            insert_query = """INSERT INTO blood_inventory(inventory_id, blood_bank_id, donor_id)
                              VALUES(%s, %s, %s)"""
            cursor.execute(insert_query, (inventory_id, blood_bank_id, donor_id))
            db.commit()
            print("Data inserted successfully into PostgreSQL!")

            # Close the cursor and database connection
            cursor.close()
            db.close()

            # Insert data into Firebase
            cred = credentials.Certificate("path/to/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            ref = firebase_db.reference('blood_inventory')  # Reference to the 'blood_inventory' node in Firebase
            ref.child(inventory_id).set({
                'blood_bank_id': blood_bank_id,
                'donor_id': donor_id
            })
            print("Data inserted successfully into Firebase!")

        except psycopg2.Error as e:
            print("Error inserting data:", e)
            db.rollback()
        finally:
            if db:
                # Close the database connection
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
    donor_records = []  # Initialize the variable with an empty list
    try:
        cursor.execute("SELECT * FROM donors WHERE donor_id = %s", (donor_id,))
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

    
def get_document_id(collection_name, field, value):
    try:
        # Initialize Firestore client
        db = firestore.client()

        # Query Firestore for documents that match the specified field and value
        query = db.collection(collection_name).where(field, '==', value).limit(1)
        results = query.get()

        # Check if any documents were found
        for doc in results:
            return doc.id  # Return the document ID

        # If no document is found, return None
        return None

    except Exception as e:
        print("Error retrieving document ID:", e)

def view_donor_firebase(donor_id):
    try:
        # Convert donor ID integer to string
        donor_id_str = str(donor_id)

        # Get the document ID from Firestore
        document_id = get_document_id('donors', 'donor_id', donor_id_str)
        
        if document_id:
            # Initialize Firestore client
            db = firestore.client()

            # Query Firestore for donor records using the retrieved document ID
            donor_ref = db.collection('donors').document(document_id)
            donor_data = donor_ref.get().to_dict()

            if donor_data:
                # Convert values to strings
                for key in donor_data:
                    donor_data[key] = str(donor_data[key])

                return [donor_data]  # Return data as a list of dictionaries
            else:
                return []  # Return an empty list if no records found
        else:
            return []  # Return an empty list if no document ID found for the given donor ID

    except Exception as e:
        print("Error viewing donor records:", e)

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
        
