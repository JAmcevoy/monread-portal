# Monread.ie: Customer Information Portal

**Objective:**  
Create a secure customer information page on Monread.ie where users can log in and access their personal information stored in our Zoho CRM system. The goal is to enable users to **view**, **update**, and **request** their information depending on their level of access.

---

## Requirements

### 1. Webpage Features

#### **Login Screen:**
- **Email Address**  
- **Password**  

#### **Post-Login Page (User Dashboard):**  
Once the user logs in, they should be able to access the following information:

- **Email**  
- **Full Name** (from CRM contact data)  
- **Company Name**  
- **Phone Number**  
- **Company Information** (Visible only if the user is an admin as marked in the CRM)  
- **Support Hours Remaining**  
- **Renewal Dates**  

*Note: Admin users will have additional privileges to view and update company-specific information.*

---

### 2. Zoho CRM Integration

#### **CRM Fields & Integration:**

- **User ID Field**: Each user should have a unique ID in the CRM, which is tied to their login credentials on the webpage. This allows data to be linked between the portal and Zoho CRM.
  
- **Is Admin Checkbox**: An “Is Admin” checkbox will be available in the CRM. When selected:
  - The user will be able to view and **update** company information.
  - Admins will have full access to company details, while non-admin users will only see their personal data and limited details.

---

### Key Considerations:

- **User Levels**: The system should recognize different levels of access (Admin, User) and restrict data accordingly.
- **Security**: The portal should have robust security measures to protect user data, especially when handling login credentials and sensitive company information.
- **Syncing Data**: Ensure real-time syncing between the webpage and Zoho CRM to reflect updates made by users on the portal.

---

**End Goal:**  
Enable a seamless user experience where users can manage their personal and company information, while admins have greater control over the company data. This solution should be secure, user-friendly, and scalable.

---
