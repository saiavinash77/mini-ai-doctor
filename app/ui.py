import streamlit as st 

def pdf_upload():
    return st.file_uploader("upload Your PDF",type = ["pdf"],accept_multiple_files = True,
                            help = "upload one or more PDF files to Process")
    
    
import streamlit as st 

# def pdf_upload():
#     st.file_uploader("Upload your pdf",type = ["pdf"],accept_multiple_files = True,
#                      help = "Upload one or more PDF files to process")
    