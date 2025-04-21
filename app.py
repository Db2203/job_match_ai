import pdfplumber
import streamlit as st
import spacy

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Function to compare resume and job description
def compare_texts(resume_text, job_description):
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)

    # Extract nouns and verbs from both the resume and job description
    resume_keywords = [token.text.lower() for token in resume_doc if token.pos_ in ['NOUN', 'VERB']]
    job_keywords = [token.text.lower() for token in job_doc if token.pos_ in ['NOUN', 'VERB']]

    # Calculate common words (keywords)
    common_keywords = set(resume_keywords) & set(job_keywords)
    return common_keywords

# Streamlit UI
st.title("Job Match AI - Resume to Job Fit Checker")

# Upload resume PDF
resume_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

# Input job description
job_description_input = st.text_area("Paste Job Description")

# If a file is uploaded and job description is entered
if resume_file is not None and job_description_input:
    # Save the uploaded file temporarily
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(resume_file.read())
    
    # Extract text from the uploaded resume
    resume_text = extract_text_from_pdf("uploaded_resume.pdf")
    
    # Compare resume text with job description
    matching_keywords = compare_texts(resume_text, job_description_input)

    # Display the extracted resume text and matching keywords
    st.subheader("Extracted Resume Text")
    st.text_area("Resume Text", resume_text, height=300)

    st.subheader("Matching Skills/Keywords")
    st.write(matching_keywords)
