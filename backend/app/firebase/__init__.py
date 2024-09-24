import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Initialize the Firebase Admin SDK
def init_firebase():
    path = os.path.abspath('serviceAccountKey.json')
    cred = credentials.Certificate(path)

    firebase_admin.initialize_app(cred)

    # Initialize Firestore and Auth if needed
    db = firestore.client()  # Firestore client
    return db

firebase_db = None

def get_firebase_db():
    global firebase_db
    if firebase_db is None:
        firebase_db = init_firebase()
    return firebase_db

def printAuth():
    try:
        # Get an iterator for the list of users from Firebase Auth
        page = auth.list_users()

        # Iterate through each user
        while page:
            for user in page.users:
                print(f'User ID: {user.uid}')
                print(f'Email: {user.email}')
                print(f'Phone Number: {user.phone_number}')
                print(f'Display Name: {user.display_name}')
                print(f'Provider Data: {user.provider_data}')
                print(f'Email Verified: {user.email_verified}')
                print('---')

            # Get the next page of users
            page = page.get_next_page()

    except Exception as e:
        print(f"Error retrieving users: {e}")
