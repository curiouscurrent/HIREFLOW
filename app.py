from dotenv import load_dotenv
# Use it
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    # Convert the pdf to image
    if uploaded_file is not None:
        pdf_content = uploaded_file.read()
        document = fitz.open(stream=pdf_content)
        page = document.load_page(0)
        pix = page.get_pixmap()
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()

            }

        ]
        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit app

st.set_page_config(page_title="HIREFLOW")
st.header("ATS TRACKER")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
