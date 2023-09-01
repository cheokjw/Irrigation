# Import Necessary Libraries
import streamlit as st
from datetime import datetime
import os
import json
from google.cloud import firestore
from google.oauth2 import service_account


# DATABASE ------------------------------------------------
# Connect to firestore database by using JSON account key
db = firestore.Client.from_service_account_json('firestore_key.json')


collections = [collection.id for collection in db.collections()]
for collection_name in collections:
    print(collection_name)
