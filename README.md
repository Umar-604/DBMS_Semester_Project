# DBMS_Semester_Project 

---

# Blood Donation Database System

## Introduction

Welcome to the Blood Donation Database System! This project is designed to organize information about blood donors, recipients, blood banks/centers, donations, and blood inventory. The system aims to facilitate the management of blood donation activities, ensuring efficient tracking of donors, recipients, blood units, and donations.

## Features

### Entities
- **Donors**: Capture information about blood donors.
- **Recipients**: Record details of blood recipients.
- **Blood Banks/Centers**: Manage information about blood banks/centers.
- **Donations**: Track blood donations and related information.
- **Blood Inventory**: Monitor the available blood units and their details.

### Relationships
- Various one-to-many and many-to-many relationships are established between entities to represent connections and interactions within the blood donation ecosystem.

### Additional Considerations
- **Security**: Proper access controls are implemented to protect sensitive information.
- **Search and Retrieval**: Users can easily search for donors, recipients, and available blood units based on different criteria.
- **Reports and Analytics**: Generate reports on blood inventory, donation trends, and other relevant metrics.
- **Data Validation**: Checks are in place to ensure data integrity and accuracy.
- **User Interface**: An intuitive user interface is designed for easy data entry and retrieval.

## Entities and Attributes

### Donors
- Donor ID
- Name
- Contact Information
- Blood Type
- Date of Birth
- Gender
- Health History
- Last Donation Date

### Recipients
- Recipient ID
- Name
- Contact Information
- Blood Type
- Date of Birth
- Gender
- Health Condition
- Hospital/Healthcare Facility

### Blood Banks/Centers
- Blood Bank ID
- Name
- Location
- Contact Information
- Services Provided
- Operating Hours

### Donations
- Donation ID
- Donor ID (Foreign Key)
- Blood Bank ID (Foreign Key)
- Donation Date
- Quantity of Blood Donated
- Blood Type
- Health Check Information

### Blood Inventory
- Inventory ID
- Blood Bank ID (Foreign Key)
- Blood Type
- Quantity Available
- Expiry Date
- Donor ID (if applicable)

##ERD 
![image](https://github.com/Umar-604/DBMS_Semester_Project/blob/main/ER_Diagram.png)

##Project Architecture
![image](https://github.com/Umar-604/DBMS_Semester_Project/blob/main/Project%20architecture.png)

##GUI
![image](https://github.com/Umar-604/DBMS_Semester_Project/blob/main/GUI.jpeg)


### Conclusion

The Blood Donation Database System presents a comprehensive solution for managing blood donation activities efficiently. By organizing information about donors, recipients, blood banks/centers, donations, and blood inventory, the system streamlines the process of tracking and managing blood-related data.

With a user-friendly frontend interface and a robust backend architecture, the system offers seamless interaction and data management capabilities. Users can easily register donors, record donations, manage blood inventory, and generate reports and analytics to gain insights into donation trends and inventory status.

Overall, the Blood Donation Database System stands as a valuable tool in the realm of healthcare management, facilitating the noble cause of blood donation and saving lives through efficient organization and utilization of blood resources.

