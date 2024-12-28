# The sidebar handles document management and model selection
import os, sys
my_folder = os.path.abspath(os.path.join(os.pardir, 'api'))
sys.path.append(my_folder)
sys.path.append(os.path.abspath(os.pardir))
import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Sidebar: Model Selection
    model_options = ["gemini-1.5-pro", "gemini-1.5-flash"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")
    
    
    # st.write(f"st.session_state.model = {st.session_state.model}")
    # st.write(f"st.session_state.model = {st.session_state.model.value}")
    
    # Sidebar: Upload Document
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html"])
    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = list_documents()  # Refresh the list after upload

    # Sidebar: List Documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        # list of documents where each document is a dictionary containing
        # filename, id and upload_timestamp
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")
        
        # Delete Document
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents()  # Refresh the list after deletion
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")