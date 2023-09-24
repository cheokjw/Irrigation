
from google.cloud import firestore
from google.oauth2 import service_account


db = firestore.Client.from_service_account_json("C:/Users/cheok/Documents/GitHub/Irrigation/firestore_key.json")
db.collection('user1').document()