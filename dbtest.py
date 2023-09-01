# Import Necessary Libraries
import streamlit as st
from datetime import datetime
import os
from google.cloud import firestore


# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
db = firestore.Client.from_service_account_json('firestore_key.json')


collections = [collection.id for collection in db.collections()]
for collection_name in collections:
    print(collection_name)
    