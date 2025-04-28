!pip install gradio spacy PyPDF2 python-docx
!python -m spacy download en_core_web_sm

import spacy
import PyPDF2
import docx
import gradio as gr
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "".join(page.extract_text() for page in reader.pages)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""

def extract_contact_info(text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    linkedin = re.findall(r"(https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+)", text)
    return email[0] if email else "", linkedin[0] if linkedin else ""

def extract_skills(text):
    keywords = [
        "python", "java", "c++", "machine learning", "data science", "django",
        "react", "sql", "html", "css", "javascript", "pandas", "numpy", "flask"
    ]
    found = [kw.title() for kw in keywords if kw in text.lower()]
    return list(set(found))

def extract_education(text):
    keywords = ["B.Tech", "M.Tech", "Bachelor", "Master", "PhD", "University", "College", "School"]
    lines = text.split("\n")
    return "\n".join([line for line in lines if any(k.lower() in line.lower() for k in keywords)])

def extract_experience(text):
    keywords = ["experience", "worked", "company", "intern", "position", "role"]
    lines = text.split("\n")
    return "\n".join([line for line in lines if any(k in line.lower() for k in keywords)])

def extract_certifications(text):
    keywords = ["certification", "certified", "certificate", "certifications"]
    lines = text.split("\n")
    return "\n".join([line for line in lines if any(k in line.lower() for k in keywords)])

def create_summary(name, skills, education):
    if not name and not skills and not education:
        return "No sufficient information found to generate summary."

    summary = f"{name} is a skilled professional with expertise in the following technologies: "

    # Check if skills are found, then add them
    if skills:
        summary += ", ".join(skills) + ". "
    else:
        summary += "no specific skills mentioned. "

    # Add education information
    if education:
        summary += f"{name} holds a {education.splitlines()[0] if education else 'unknown degree'}."
    else:
        summary += "No educational details found."

    return summary

def check_missing_sections(name, email, linkedin, skills, education, experience, certifications):
    feedback = []
    if not name:
        feedback.append("⚠ Name is missing.")
    if not email:
        feedback.append("⚠ Email is missing.")
    if not linkedin:
        feedback.append("⚠ LinkedIn profile is missing.")
    if not skills:
        feedback.append("⚠ No skills found. Add your technical or soft skills.")
    if not education:
        feedback.append("⚠ Education details are missing.")
    if not experience:
        feedback.append("⚠ Work experience not found.")
    if not certifications:
        feedback.append("⚠ Certifications not found.")
    return "\n".join(feedback) if feedback else "✅ Your resume contains all major sections."

def process_resume(file):
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return "Unsupported file format", "", "", "", "", "", "", "", ""

    name = extract_name(text)
    email, linkedin = extract_contact_info(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    certifications = extract_certifications(text)
    summary = create_summary(name, skills, education)
    feedback = check_missing_sections(name, email, linkedin, skills, education, experience, certifications)

    return name or "Not found", email or "Not found", linkedin or "Not found", \
           ", ".join(skills) if skills else "Not found", education or "Not found", \
           experience or "Not found", certifications or "Not found", summary, feedback

with gr.Blocks() as demo:
    gr.Markdown("## 📄 Smart Resume Scanner")
    gr.Markdown("Upload your resume and get suggestions on what's missing! 👇")

    with gr.Row():
        file_input = gr.File(label="📁 Upload PDF or DOCX Resume")

    with gr.Row():
        name_box = gr.Textbox(label="👤 Name")
        email_box = gr.Textbox(label="📧 Email")
        linkedin_box = gr.Textbox(label="🔗 LinkedIn Profile")

    skills_box = gr.Textbox(label="💼 Skills")
    education_box = gr.Textbox(label="🎓 Education", lines=3)
    experience_box = gr.Textbox(label="🏢 Experience", lines=3)
    certifications_box = gr.Textbox(label="📜 Certifications", lines=3)
    summary_box = gr.Textbox(label="📝 Summary", lines=2)
    feedback_box = gr.Textbox(label="🔎 Missing Sections Feedback", lines=4)

    btn = gr.Button("🔍 Analyze Resume")

    btn.click(
        fn=process_resume,
        inputs=[file_input],
        outputs=[
            name_box, email_box, linkedin_box,
            skills_box, education_box, experience_box,
            certifications_box, summary_box, feedback_box
        ]
    )

demo.launch(share=True)
