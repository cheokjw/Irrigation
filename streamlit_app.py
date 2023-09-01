import streamlit as st
# from google.cloud import firestore


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)

# # Connect to firestore database by using JSON account key
# db = firestore.Client.from_service_account_json("firestore_key.json")

# ref = db.collection("plant").document("plantData")

# # Obtain data from the collection
# doc = ref.get()

# # Display obtained data
# st.header("Smart Irrigation System")
# st.write(f"The id is {doc.id}")
# st.write(f"The contents are {doc.to_dict()}")