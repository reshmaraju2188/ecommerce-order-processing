import logging
import uuid
import pyodbc
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from urllib.parse import parse_qs

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="order")
def order(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a new order request...')

    try:
        # Read and parse form data manually
        raw_body = req.get_body().decode()
        logging.info(f"Raw request body: {raw_body}")

        form_data = parse_qs(raw_body)
        logging.info(f"Parsed form data: {form_data}")

        name = form_data.get('name', [''])[0]
        email = form_data.get('email', [''])[0]
        address = form_data.get('address', [''])[0]
        product = form_data.get('product', [''])[0]
        quantity = form_data.get('quantity', [''])[0]

        payment_status = "Paid"
        tracking_code = "ORD-" + str(uuid.uuid4())[:8]

        # Validate input
        if not all([name, email, address, product, quantity]):
            return func.HttpResponse("Missing required fields.", status_code=400)

        # Access Azure Key Vault
        kv_url = "https://ecommerceKeyV.vault.azure.net/"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_url, credential=credential)

        sql_user = client.get_secret("sqlusr").value
        sql_pass = client.get_secret("sqlpasswrd").value
        sql_server = "eautos.database.windows.net"
        sql_database = "ecommerceDB"

        # Connect to SQL
        conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={sql_server};DATABASE={sql_database};UID={sql_user};PWD={sql_pass}"
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Orders (CustomerName, Email, Address, ProductName, Quantity, PaymentStatus, TrackingCode)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, name, email, address, product, int(quantity), payment_status, tracking_code)
            conn.commit()

        return func.HttpResponse(f"Order placed successfully! Your tracking code is: {tracking_code}", status_code=200)

    except Exception as e:
        logging.error(f"🔥 Exception occurred: {str(e)}")
        return func.HttpResponse("Order failed. Please try again later.", status_code=500)
