# 🎓 Student Skill Gap Analyzer

A web-based career development platform that helps students analyze their resumes, identify career-related skill gaps, generate personalized learning roadmaps, and track their progress toward their career goals.

---

## 📌 Overview

Students often know the career they want to pursue but struggle to understand:

* What skills are required for that career
* Which skills they already possess
* Which skills they are missing
* How strong their resume is
* What they should learn next

The **Student Skill Gap Analyzer** addresses these challenges through a single platform that combines:

* User authentication
* Resume analysis
* ATS-style resume scoring
* Skill gap identification
* Personalized learning roadmaps
* Progress analytics
* Profile management

The application provides students with a structured way to understand their current capabilities and plan their next steps toward becoming career-ready.

---

## ✨ Features

### 🔐 Authentication

The application provides a complete user authentication flow.

* User signup
* User login
* Password hashing
* Session management
* User-specific data handling
* Data reset functionality

---

### 📄 Resume Score Analysis

Users can analyze their resume by:

* Uploading a PDF resume
* Pasting resume text directly

The system analyzes the provided resume and generates an ATS-style score along with improvement suggestions.

#### Resume Analysis Includes

* Resume score
* Skill-related analysis
* Resume content evaluation
* Improvement suggestions
* Areas that can be strengthened

---

### 🧠 Skill Gap Analysis

Users can select a target career role and analyze the difference between their existing skills and the skills required for that role.

The system identifies:

* Matched skills
* Missing skills
* Skill match percentage
* Areas requiring improvement

This helps users understand exactly which skills they should focus on developing.

---

### 🛤️ Personalized Learning Roadmap

Based on the identified skill gaps, the application generates a structured learning roadmap.

The roadmap is organized into progressive levels:

```text
Beginner
    ↓
Intermediate
    ↓
Advanced
```

This allows users to follow a structured learning journey instead of trying to learn everything at once.

---

### 📊 Progress Analytics

The analytics section provides visual insights into the user's career preparation progress.

It includes analytics related to:

* Skill matching
* Resume score
* Learning progress
* Skill improvement

This allows users to track their progress and understand their development over time.

---

### 👤 Profile Management

Users can:

* View their profile
* Edit profile information
* Manage their stored data
* Reset their application data

---

## 🔄 Application Workflow

```text
┌──────────────┐
│    Signup    │
└──────┬───────┘
       ▼
┌──────────────┐
│    Login     │
└──────┬───────┘
       ▼
┌──────────────┐
│  Dashboard   │
└──────┬───────┘
       ▼
┌────────────────────┐
│ Upload or Paste    │
│ Resume Content     │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Resume Score &     │
│ Analysis           │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Select Target      │
│ Career Role        │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Skill Gap Analysis │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Learning Roadmap   │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Analytics &        │
│ Progress Tracking  │
└────────────────────┘
```

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │   Streamlit Web UI  │
                    └──────────┬──────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐        ┌───────────────┐       ┌───────────────┐
│    Auth     │        │ Resume Scorer │       │ Skill Analyzer│
│   Module    │        │    Module     │       │    Module     │
└──────┬──────┘        └───────┬───────┘       └──────┬────────┘
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               ▼
                     ┌───────────────────┐
                     │ Roadmap Generator │
                     └─────────┬─────────┘
                               ▼
                     ┌───────────────────┐
                     │ Analytics Module  │
                     └─────────┬─────────┘
                               ▼
                     ┌───────────────────┐
                     │   JSON Storage    │
                     └───────────────────┘
```

---

## 📁 Project Structure

```text
skill_gap_analyzer/
│
├── app.py
│   └── Main application landing page
│
├── pages/
│   ├── 1_Login.py
│   │   └── Login page
│   │
│   ├── 2_Signup.py
│   │   └── User registration page
│   │
│   ├── 3_Dashboard.py
│   │   └── Main user dashboard
│   │
│   ├── 4_Resume_Score.py
│   │   └── Resume upload and ATS-style scoring
│   │
│   ├── 5_Skill_Gap.py
│   │   └── Skill gap analysis
│   │
│   ├── 6_Roadmap.py
│   │   └── Personalized learning roadmap
│   │
│   ├── 7_Analytics.py
│   │   └── Progress analytics
│   │
│   └── 8_Profile.py
│       └── User profile management
│
├── components/
│   └── navbar.py
│       └── Reusable navigation component
│
├── utils/
│   ├── auth.py
│   │   └── Authentication and session management
│   │
│   ├── scorer.py
│   │   └── Resume scoring logic
│   │
│   ├── analyzer.py
│   │   └── Skill gap analysis logic
│   │
│   └── roadmap.py
│       └── Learning roadmap generation
│
├── data/
│   └── users.json
│       └── Application data storage
│
├── requirements.txt
│   └── Project dependencies
│
└── README.md
    └── Project documentation
```

---

## 🛠️ Technology Stack

### Application Framework

* **Streamlit**

### Programming Language

* **Python**

### Resume Processing

* **pdfplumber**

### Data Processing

* **pandas**

### Data Storage

* **JSON**

### Data Visualization

* **Streamlit Charts**

### Authentication

* Password hashing
* Session management

---

## ⚙️ Installation

### Prerequisites

Make sure the following are installed:

* Python 3.x
* pip

---

### 1. Clone the Repository

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd skill_gap_analyzer
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

```bash
streamlit run app.py
```

---

### 5. Open the Application

Open the following address in your browser:

```text
http://localhost:8501
```

---

## 💡 How It Works

### 1. Create an Account

The user creates an account using the signup page.

### 2. Log In

The user logs in using their registered credentials.

### 3. Analyze a Resume

The user can either upload a PDF resume or paste resume content.

### 4. Review the Resume Score

The application analyzes the resume and provides an ATS-style score with suggestions.

### 5. Select a Target Career Role

The user selects the career role they want to pursue.

### 6. Analyze Skill Gaps

The application compares the user's skills with the skills associated with the selected role.

### 7. Follow the Learning Roadmap

The user receives a structured roadmap based on the identified skill gaps.

### 8. Track Progress

The user can view their progress through the analytics section.

---

## 📊 Core Modules

| Module            | Responsibility                                |
| ----------------- | --------------------------------------------- |
| Authentication    | Signup, login, password hashing, and sessions |
| Resume Scorer     | Resume processing and ATS-style scoring       |
| Skill Analyzer    | Matched and missing skill identification      |
| Roadmap Generator | Structured learning path generation           |
| Analytics         | Progress visualization and tracking           |
| Profile           | User profile and data management              |

---

## 🔒 Data Storage

The application currently uses a JSON-based storage system.

User data is stored in:

```text
data/users.json
```

This approach makes the application simple to set up and suitable for local development and academic project demonstrations.

For a production-scale deployment, the storage layer can be replaced with a dedicated database system.

---

## 🎯 Project Objectives

The project was developed to:

* Help students understand their current skill set
* Identify gaps between existing and required skills
* Analyze resumes and provide improvement suggestions
* Generate structured learning roadmaps
* Help students monitor their career preparation progress
* Provide a centralized platform for career skill development

---

## 🌟 Project Highlights

* Complete multi-page Streamlit application
* Modular project architecture
* Reusable UI components
* Separate utility modules for core business logic
* PDF resume processing
* Resume scoring system
* Skill matching and gap detection
* Personalized roadmap generation
* User authentication
* Progress analytics
* Profile management

---

## 🚀 Future Scope

The application can be extended with:

* AI-powered resume analysis
* Automated skill extraction from resumes
* Machine learning-based career recommendations
* Integration with online learning platforms
* Course recommendations for missing skills
* Job and internship recommendations
* Real-time industry skill demand analysis
* Database integration
* Cloud deployment
* Advanced user and administrator dashboards

---

## 📌 Project Status

### ✅ Completed

* User authentication
* Signup and login
* Password hashing
* Session management
* Resume PDF upload
* Resume text input
* Resume scoring
* Resume improvement suggestions
* Target role selection
* Skill gap analysis
* Matched skill identification
* Missing skill identification
* Learning roadmap generation
* Analytics dashboard
* Profile management
* Data reset functionality

---

## 🎓 Project Significance

The **Student Skill Gap Analyzer** addresses the gap between a student's current technical capabilities and the skills expected in their desired career path.

Instead of providing generic career advice, the application helps students follow a structured process:

```text
Understand Current Skills
          ↓
Analyze Resume
          ↓
Identify Skill Gaps
          ↓
Create Learning Roadmap
          ↓
Track Progress
          ↓
Move Toward Career Readiness
```

The project demonstrates the practical use of Python, Streamlit, PDF processing, authentication, data analysis, and modular software design to create a complete career development application.

---

## 👩‍💻 Author

**Mahathi Godala**

Computer Science Engineering Student

---

## 📄 License

This project was developed for educational and academic purposes.

---

<p align="center">
  <b>Student Skill Gap Analyzer</b>
  <br>
  Helping students understand their skills, identify their gaps, and build a structured path toward their career goals.
</p>
