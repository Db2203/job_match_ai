import pdfplumber
import streamlit as st
import spacy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text

nlp = spacy.load("en_core_web_sm")

def compare_texts(resume_text, job_description):
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)
    resume_keywords = [token.text.lower() for token in resume_doc if token.pos_ in ['NOUN', 'VERB']]
    job_keywords = [token.text.lower() for token in job_doc if token.pos_ in ['NOUN', 'VERB']]
    common_keywords = set(resume_keywords) & set(job_keywords)
    return common_keywords

def generate_pdf_report(matching_keywords):
    file_name = "matching_keywords_report.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, "Job Match AI - Matching Skills/Keywords Report")
    c.drawString(100, 730, "Matching Keywords:")
    y_position = 710
    for keyword in matching_keywords:
        c.drawString(100, y_position, f"- {keyword}")
        y_position -= 20
    c.save()
    return file_name

st.title("Job Match AI - Resume to Job Fit Checker")

resume_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")
job_description_input = st.text_area("Paste Job Description")

if resume_file is not None and job_description_input:
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(resume_file.read())
    
    resume_text = extract_text_from_pdf("uploaded_resume.pdf")
    matching_keywords = compare_texts(resume_text, job_description_input)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Text", resume_text, height=300)

    st.subheader("Matching Skills/Keywords")
    st.write(matching_keywords)

    if st.button("Generate PDF Report"):
        pdf_file = generate_pdf_report(matching_keywords)
        st.download_button(
            label="Download PDF Report",
            data=open(pdf_file, "rb").read(),
            file_name=pdf_file,
            mime="application/pdf"
        )
