# Group Members:-

- Neel Jogani:- KU2407U094
- Helin Patel:- KU2407U072
- Dhruvil Patel:- Ku2407U052


# Smart Resume Scanner

This project uses AI to extract and analyze information from resumes (PDF and DOCX formats). It can extract key sections such as:

- Name
- Email
- LinkedIn Profile
- Skills
- Education
- Experience
- Certifications

## Requirements

- Python 3.x
- Install dependencies using `pip install -r requirements.txt`

## Web Link
https://ec459577b895b5e48c.gradio.live/

## Running the Application

Run the app with the following command:

```bash
python app.py

Smart Resume Scanner
The Smart Resume Scanner is an AI-powered tool that extracts and analyzes key sections from resumes in PDF or DOCX formats. It provides feedback on missing sections and generates a summary based on the resume content.

Libraries and Dependencies
spaCy: For NLP, to extract names and process text.

PyPDF2: To extract text from PDF files.

python-docx: To extract text from DOCX files.

re: For extracting emails and LinkedIn profiles using regular expressions.

gradio: To create a simple web interface.

Key Functions
Text Extraction: Extracts text from PDF or DOCX files.

Information Extraction:

extract_name: Extracts the person’s name.

extract_contact_info: Extracts email and LinkedIn profile.

extract_skills: Detects technical skills from a predefined list.

extract_education: Extracts educational details.

extract_experience: Extracts work experience details.

extract_certifications: Extracts certification information.

Summary Creation: Generates a summary based on the name, skills, and education.

Feedback: Provides feedback on missing sections (name, email, skills, etc.).

Gradio Interface
Upload your resume (PDF/DOCX) and get extracted details in textboxes: Name, Email, LinkedIn, Skills, Education, Experience, Certifications, and Feedback on missing sections.

Button: Triggers analysis when clicked.

How to Run
Clone the repository.

Install dependencies: pip install -r requirements.txt.

Run the app: python app.py.

Open the provided URL to use the tool.
