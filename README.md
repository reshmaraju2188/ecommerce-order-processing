PROJECT Title - E-commerce Order Processing

Objective: Build a cloud-native order processing system using serverless architecture and secure database connectivity.
Tech Stack: Azure Functions (Python), Azure SQL Database, Azure Key Vault, Azure Static Web Apps (HTML/CSS/JS), Azure DevOps/GitHub for CI/CD
Outcome: Accept customer orders from a frontend form, securely store them in Azure SQL DB using managed identity and secrets, and provide real-time order placement.

Architecture Flow:

1. Frontend – Azure Static Web App
Technology: HTML + CSS + JS
Role: Displays a user-friendly Order Form.
Hosted on: Azure Static Web Apps
User Action: Customer enters order details and clicks "Place Order".


2. HTTP Request → Azure Function (API)
The form submission sends a POST request to:
Data like name, email, product, quantity, etc., is sent to the backend.
3. Backend – Azure Function App (Python)
Tech Used: Python (Azure Function)
Role:
Receives the order.
Validates required fields.
Creates a unique tracking code.
Retrieves SQL credentials from Azure Key Vault.
Inserts order into Azure SQL Database.
4. Azure Key Vault
Stores:
sqlusr – SQL username
sqlpasswrd – SQL password
Used to securely fetch credentials via Managed Identity.
Only Azure Function (via Managed Identity) can access secrets.
5. Azure SQL Database
Stores the order data in a table Orders.
Fields include:
CustomerName, Email, ProductName, TrackingCode, etc.
You can query the database to:
View customer orders.
Track order history.
