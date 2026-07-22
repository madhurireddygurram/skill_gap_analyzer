# 🎓 Student Skill Gap Analyzer

> **An integrated career-readiness platform that helps students build professional resumes, analyze their skills, identify career gaps, and follow personalized learning roadmaps.**

---

## 📌 Overview

The **Student Skill Gap Analyzer** is a Streamlit-based web application designed to help students understand their career readiness and take structured steps toward their desired career path.

The platform combines **resume building, resume analysis, skill gap detection, personalized learning roadmaps, progress analytics, and profile management** into one application.

It helps students move from:

```text
Build Resume
     ↓
Analyze Resume
     ↓
Identify Skill Gaps
     ↓
Follow Learning Roadmap
     ↓
Track Progress
```

---

## ✨ Features

### 🔐 Authentication

* User signup and login
* Password hashing
* Session management
* User-specific data handling

### 🧾 Resume Builder

Create and organize a professional resume with sections such as:

* Personal Information
* Professional Summary
* Education
* Technical Skills
* Work Experience
* Projects
* Certifications
* Achievements

### 📄 Resume Score Analyzer

* Upload PDF resumes
* Paste resume text
* Generate ATS-style resume scores
* Analyze resume content
* Provide improvement suggestions

### 🧠 Skill Gap Analyzer

* Select a target career role
* Identify matched skills
* Detect missing skills
* View skill match progress

### 🛤️ Personalized Roadmap

Generate structured learning paths based on missing skills:

```text
Beginner → Intermediate → Advanced
```

### 📊 Analytics

Track:

* Skill match progress
* Resume score
* Learning progress
* Skill development

### 👤 Profile Management

* View and edit profile information
* Manage user data
* Reset application data

---

## 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **pdfplumber**
* **pandas**
* **JSON**
* **Streamlit Charts**

---

## 🏗️ Project Structure

```text
skill_gap_analyzer/
│
├── app.py
│
├── pages/
│   ├── 1_Login.py
│   ├── 2_Signup.py
│   ├── 3_Dashboard.py
│   ├── 4_Resume_Score.py
│   ├── 5_Skill_Gap.py
│   ├── 6_Roadmap.py
│   ├── 7_Analytics.py
│   ├── 8_Profile.py
│   └── 9_Resume_Builder.py
│
├── components/
│   └── navbar.py
│
├── utils/
│   ├── auth.py
│   ├── scorer.py
│   ├── analyzer.py
│   └── roadmap.py
│
├── data/
│   └── users.json
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd skill_gap_analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🔄 Application Workflow

```text
Sign Up / Login
      ↓
Dashboard
      ↓
Build or Upload Resume
      ↓
Resume Score Analysis
      ↓
Select Target Career Role
      ↓
Skill Gap Analysis
      ↓
Personalized Learning Roadmap
      ↓
Progress Analytics
```

---

## 📊 Core Modules

| Module            | Description                                     |
| ----------------- | ----------------------------------------------- |
| Authentication    | Signup, login, password hashing, and sessions   |
| Resume Builder    | Create and organize professional resume content |
| Resume Scorer     | Analyze resumes and generate ATS-style scores   |
| Skill Analyzer    | Identify matched and missing skills             |
| Roadmap Generator | Generate structured learning paths              |
| Analytics         | Track career preparation progress               |
| Profile           | Manage user profile and application data        |

---

## 🎯 Project Objectives

* Help students create professional resumes
* Analyze resume quality and provide suggestions
* Identify gaps between current and required career skills
* Generate personalized learning paths
* Track progress toward career readiness
* Provide a centralized platform for student career development

---

## 🚀 Future Scope

* AI-powered resume analysis
* Automated skill extraction
* Personalized course recommendations
* Job and internship recommendations
* Real-time industry skill analysis
* Database integration
* Cloud deployment
* Advanced career recommendation systems

---

## 📌 Project Status

### ✅ Completed

* User Authentication
* Signup and Login
* Password Hashing
* Session Management
* Resume Builder
* Resume PDF Upload
* Resume Text Analysis
* ATS-Style Resume Scoring
* Resume Improvement Suggestions
* Target Career Role Selection
* Skill Gap Analysis
* Matched Skill Detection
* Missing Skill Detection
* Personalized Learning Roadmaps
* Progress Analytics
* Profile Management
* Data Reset Functionality

---

## 👩‍💻 Contributors

### Mahathi Godala

Computer Science Engineering Student

### Madhuri Gurram

Computer Science Engineering Student

---

## 📄 License

This project was developed for educational and academic purposes.

---

<p align="center">
  <b>Student Skill Gap Analyzer</b>
  <br>
  Build your resume. Discover your gaps. Learn what matters. Become career-ready.
</p>
