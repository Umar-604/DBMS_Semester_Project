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
def insert_donor(donor_id, name, contact, blood_type, date_of_birth, gender, health_history, last_donation_date):

    db=get_db_connection()
    if db:
        try:
            cursor =db.cursor()
            insert_query="""INSERT INTO donors(donor_id, name, contact, blood_type, date_of_birth, gender, health_history, last_donation_date)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (donor_id, name, contact, blood_type, date_of_birth, gender, health_history, last_donation_date))
            db.commit()
            print("Donor's data inserted successfully!")
        except psycopg2.Error as e:
            print("Error inserting donor data:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

# Function to recieve donor data into the database
def insert_receiver():
    recipent_id=input("Enter recipent ID:")
    name=input("Enter name:")
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
            insert_query="""INSERT INTO recipients(recipient_id, name, contact, blood_type, date_of_birth, gender, health_history, hospital)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (recipent_id, name, contact, blood_type, date_of_birth, gender, health_history, hospital))
            db.commit()
            print("Receiver's data inserted successfully!")
        except psycopg2.Error as e:
            print("Error inserting recipient data:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

def insert_blood_bank():
    blood_bank_id = input("Enter blood bank ID : ")
    name = input("Enter name of blood bank : ")
    location = input("Enter location of blood bank : ")
    contact = input("Enter contact info of blood bank :")
    services_provided = input("Enter the services provided by blood bank : ")
    operating_hours = input("Enter operating hours : ")

    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            insert_query = """INSERT INTO blood_banks(blood_bank_id, name, location, contact, services_provided, operating_hours)
                              VALUES(%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (blood_bank_id, name, location, contact, services_provided, operating_hours))
            db.commit()
            print("Blood bank inserted successfully!")
        except psycopg2.Error as e:
            print("Error inserting data:", e)
            db.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()


def insert_donations():
    donor_id = input("Enter donor's ID : ")
    blood_bank_id = input("Enter blood bank ID : ")
    quantity_donated = input("Enter quantity of blood(ml) : ")
    blood_type = input("Enter blood type : ")
    health_check_information = input("Enter health check information : ")

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

def insert_blood_inventory():
    inventory_id = input("Enter Inventory ID : ")
    blood_bank_id = input("Enter Blood Bank ID : ")
    donor_id = input("Enter donor ID : ")

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


def view_table_data(table_name):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()
    db.close()
    return rows
#table_name = input("Enter table name : ")
#data = view_donor_data(table_name)
#for row in data:
 #   print(row)            
# Call the insert_donor function
# insert_donor()
# insert_receiver()
# insert_blood_bank()
# insert_donations()
# insert_blood_bank()
# insert_blood_inventory()