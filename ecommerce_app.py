import csv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Sample in-memory database
users = []
products = []

class User:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

class Product:
    def __init__(self, name, barcode, brand, description, price, available):
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.description = description
        self.price = price
        self.available = available

class ECommerceAPI(BaseHTTPRequestHandler):

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/register':
            self.register_user()
        elif path == '/api/login':
            self.login()
        elif path == '/api/upload-product-csv':
            self.upload_product_csv()
        elif path.startswith('/api/products/'):
            self.product_review()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/products':
            self.list_products()
        else:
            self.send_response(404)
            self.end_headers()

    def register_user(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        user_data = json.loads(data.decode('utf-8'))

        # Perform validation here (e.g., check if username is unique)

        user = User(user_data['first_name'], user_data['last_name'], user_data['username'], user_data['password'])
        users.append(user)

        self.send_response(201)
        self.end_headers()

    def login(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        login_data = json.loads(data.decode('utf-8'))

        # Perform validation and authentication here (e.g., check username and password)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Login successful"}).encode('utf-8'))

    def upload_product_csv(self):
        # Implement CSV file handling and product creation here
        # You can use libraries like 'csv' to parse the uploaded CSV file

        self.send_response(201)
        self.end_headers()

    def product_review(self):
        parsed_path = urlparse(self.path)
        product_id = int(parsed_path.path.split('/')[-1])

        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        review_data = json.loads(data.decode('utf-8'))

        # Implement product review logic here, associating it with the specified product_id

        self.send_response(201)
        self.end_headers()

    def list_products(self):
        # Implement pagination and sorting logic here

        # Sample data for demonstration (replace with actual product data)
        sample_products = [
            Product("Product 1", "34567890", "Brand 1", "This is sample description", 200, True),
            # Add more sample products here
        ]

        products_data = []
        for product in sample_products:
            product_data = {
                "name": product.name,
                "barcode": product.barcode,
                "brand": product.brand,
                "description": product.description,
                "price": product.price,
                "available": product.available
            }
            products_data.append(product_data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(products_data).encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), ECommerceAPI)
    print('Server started on http://localhost:8080')
    server.serve_forever()
