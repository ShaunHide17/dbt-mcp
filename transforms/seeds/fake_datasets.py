from faker import Faker
import random
import uuid
import pandas as pd

fake = Faker()

def generate_data():

    # CUSTOMERS
    num_customers = random.randint(100, 1000)
    customers = [
        {
            "id": str(uuid.uuid4()),
            "salutation": fake.random_element(elements=('Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.')),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "updated_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
        }
        for _ in range(num_customers)
    ]
    customers_df = pd.DataFrame(customers)
    customers_df.to_csv('customers.csv', index=False)

    # PRODUCTS
    num_products = random.randint(50, 100)
    categories = ['Electronics', 'Clothing', 'Books', 'Toys', 'Furniture', 'Other']
    products = [
        {
            "id": str(uuid.uuid4()),
            "name": fake.word(),
            "brand": fake.company(),
            "category": fake.random_element(elements=categories),
            "description": fake.text(),
            "price": fake.random_int(min=10, max=1000),
            "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "updated_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
        }
        for _ in range(num_products)
    ]
    products_df = pd.DataFrame(products)
    products_df.to_csv('products.csv', index=False)

    # STORES
    num_stores = 7
    stores = [
        {
            "id": str(uuid.uuid4()),
            "name": fake.company(),
            "address": fake.address(),
            "city": fake.city(),
            "postcode": fake.postcode(),
            "country": fake.country(),
            "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "updated_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
        }
        for _ in range(num_stores)
    ]
    stores_df = pd.DataFrame(stores)
    stores_df.to_csv('stores.csv', index=False)

    # TRANSACTIONS
    num_transactions = random.randint(100000, 150000)
    transactions = [
        {
            "id": str(uuid.uuid4()),
            "customer_id": fake.random_element(elements=customers_df['id']),
            "product_id": fake.random_element(elements=products_df['id']),
            "store_id": fake.random_element(elements=stores_df['id']),
            "transaction_date": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "amount": round(random.random() * 500, 2),
            "currency": fake.currency_code(),
            "payment_method": fake.random_element(elements=('Credit Card', 'Debit Card', 'Cash', 'Other')),
            "payment_status": fake.random_element(elements=('Pending', 'Completed', 'Failed')),
            "payment_reference": fake.uuid4(),
        }
        for _ in range(num_transactions)
    ]
    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv('transactions.csv', index=False)

    return {
        'customers': customers_df.shape,
        'products': products_df.shape,
        'stores': stores_df.shape,
        'transactions': transactions_df.shape,
    }

if __name__ == "__main__":
    print(generate_data())