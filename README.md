# AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes against ATS (Applicant Tracking Systems) and provides actionable feedback to improve job applications. The application allows users to upload PDF resumes, analyzes them using a locally running Large Language Model (Ollama), stores previous analyses in a SQLite database, and presents the results through an intuitive Streamlit interface.


## Features

- Upload PDF resumes
- AI-powered resume analysis using Ollama
- Resume quality score
- ATS compatibility score
- Skills score
- Strengths and weaknesses analysis
- Missing skills detection
- Personalized recommendations
- Resume history
- Delete previous analyses
- Responsive Streamlit dashboard
- Docker support


## Tech Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Ollama
- PyMuPDF

### Frontend

- Streamlit

### AI

- Ollama
- Qwen 2.5 (Manually configurable)

### Deployment

- Docker
- Docker Compose


## Analysis Workflow

1. User uploads a PDF resume.
2. The backend extracts text from the document.
3. A prompt is generated for the LLM.
4. Ollama analyzes the resume.
5. The response is parsed into structured JSON.
6. Results are stored in SQLite.
7. Analysis is displayed in the dashboard.
8. Previous analyses can be viewed or deleted.

## Scores

### Resume Score

Evaluates:

- Resume structure
- Formatting
- Readability
- Overall quality

### ATS Score

Evaluates:

- ATS compatibility
- Keywords
- Resume parsing quality
- Section organization

### Skills Score

Evaluates:

- Technical skills
- Relevant technologies
- Experience alignment
- Missing competencies

## Running with Docker

### Clone the repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Start Ollama

Install Ollama first:

https://ollama.com

Run:

```bash
ollama serve
```

Download a model:

```bash
ollama pull llama3.2
```

---

### Start the application

```bash
docker compose up --build
```

Frontend

```
http://localhost:8501
```

Backend

```
http://localhost:8000/docs
```

---

## Running Without Docker

Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

---

Frontend

```bash
cd frontend

pip install -r requirements.txt

streamlit run Home.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|----------|--------------------|---------------------------|
| POST | `/resume/upload` | Upload a resume |
| GET | `/resume/history` | Retrieve analysis history |
| DELETE | `/resume/{id}` | Delete a resume |
| GET | `/docs` | Swagger documentation |


## License

This project is licensed under the MIT License.