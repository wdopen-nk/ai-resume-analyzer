# AI Resume Analyzer

An AI-powered web application that analyzes resumes, evaluates ATS compatibility, identifies strengths and weaknesses, and compares resumes against job descriptions.

Built with FastAPI, Streamlit, Ollama, and SQLite, the application provides a complete resume analysis workflow with user authentication, analysis history, and AI-powered job matching.

## Features

### AI Resume Analysis

Upload a resume in PDF or DOCX format and receive an AI-generated analysis including:

- Overall Resume Score
- ATS Compatibility Score
- Skills Score
- Resume Strengths
- Resume Weaknesses
- Missing Skills
- Personalized Recommendations

### AI Job Matcher

Compare an analyzed resume against a job description and receive:

- Overall Match Score
- Skills Match Score
- Experience Match Score
- Keyword Match Score
- Matching Skills
- Missing Skills
- Matching Keywords
- Missing Keywords
- Personalized Improvement 
- Recommendations

### Authentication & Authorization

The application supports secure multi-user functionality:

- User Registration
- User Login
- JWT Authentication
- Password Hashing
- Protected API Endpoints
- User-specific Resume History
- Authorization checks to prevent users from accessing other users' data

### Resume History

Users can:

- View previously analyzed resumes
- Review detailed analysis results
- Access previous job matches
- Delete resumes and associated analyses

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Password Hashing
- Pydantic

### Frontend

- Streamlit
- Requests

### AI

- Ollama
- Large Language Models for resume analysis and job matching

### Document Processing

- PDF parsing
- DOCX parsing

### DevOps

- Docker
- Docker Compose

## Getting Started

### 1. Clone the repository

```
git clone https://github.com/wdopen-nk/ai-resume-analyzer.git

cd ai-resume-analyzer
```

### 2. Install and Run Ollama

Install Ollama from the official website.

After installation, pull the model used by the application:

```
ollama pull qwen2.5:7b
```

Start Ollama:

```
ollama serve
```

If Ollama is running on your host machine while the backend runs inside Docker, the backend communicates with Ollama through:

```
host.docker.internal:11434
```

### 3. Configure Environment Variables

Create a `.env` file if required:

```
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Start the application with Docker

Build and start all services:

```
docker compose up --build
```

### Access the application

After starting Docker, open:

#### Frontend

```
http://localhost:8501
```
#### Backend API

```
http://localhost:8000
```

#### Swagger Documentation

```
http://localhost:8000/docs
```

The application will start the backend and frontend containers.

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

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|----------|--------------------|---------------------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and recieve JWT token |

### Resume

| Method | Endpoint | Description |
|----------|--------------------|---------------------------|
| POST | `/resume/upload` | Register a new user |
| GET | `/resume/history` | Login and recieve JWT token |
| GET | `/resume/{resume_id}` | Register a new user |
| DELETE | `/resume/{resume_id}` | Login and recieve JWT token |

### Job Matching

| Method | Endpoint | Description |
|----------|--------------------|---------------------------|
| POST | `/resume/match` | Register a new user |
| GET | `/resume/{resume_id}/matches` | Login and recieve JWT token |

Note: All resume and job matching endpoints require authentication.

## License

This project is licensed under the MIT License.