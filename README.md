# DPDP Act 2023 Compliance Checker 🔒

## Project Overview

A full-stack web application that analyzes privacy policies for compliance with **India's Digital Personal Data Protection (DPDP) Act 2023**. The system uses AI-powered semantic analysis to evaluate privacy documents and automatically generate comprehensive compliance reports.

### Key Features 🎯
- ✅ **AI-Powered Analysis**: Semantic similarity matching using Sentence Transformers
- ✅ **Compliance Scoring**: Automatic DPDP clause compliance percentage calculation
- ✅ **Risk Assessment**: Smart risk classification (Low/Medium/High)
- ✅ **Dual Input Methods**: Upload files or analyze privacy policy URLs
- ✅ **PDF Reports**: Generate downloadable compliance reports
- ✅ **Visual Charts**: Clause-by-clause compliance breakdown charts
- ✅ **Database Persistence**: SQLAlchemy ORM with report history
- ✅ **Docker Containerization**: Production-ready containerization
- ✅ **CI/CD Pipeline**: Jenkins automation for deployment
- ✅ **Git Version Control**: Full GitHub integration

---

## Architecture 🏗️

### Technology Stack

**Backend**
- Framework: FastAPI
- Python: 3.x
- AI Engine: Sentence Transformers (Semantic analysis)
- Database: SQLAlchemy ORM
- Reports: ReportLab (PDF), Matplotlib (Charts)
- Web Scraping: BeautifulSoup4
- Server: Uvicorn

**Frontend**
- Framework: React 19
- Build Tool: Vite
- Styling: Tailwind CSS
- Animations: Framer Motion
- HTTP Client: Axios
- Routing: React Router
- Charts: Chart.js

**DevOps**
- Containerization: Docker & Docker Compose
- CI/CD: Jenkins
- Version Control: Git/GitHub
- Public Access: ngrok

---

## Project Structure 📁

```
dpdp-compliance-checker/
├── dpdp-backend/
│   ├── main.py                 # Basic API endpoints
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container
│   ├── api/
│   │   ├── routes.py          # Advanced API endpoints
│   │   └── auth.py            # Authentication
│   ├── services/
│   │   ├── scoring_engine.py   # AI compliance analysis
│   │   ├── report_generator.py # PDF report generation
│   │   ├── crawler.py          # URL policy fetching
│   │   └── nlp_analyzer.py     # NLP processing
│   ├── models/
│   │   └── compliance_model.py # Database models
│   ├── database/
│   │   └── db.py              # Database configuration
│   └── core/
│       └── config.py           # Settings
│
├── dpdp-frontend/
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── Dockerfile              # Frontend container
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Root component
│   │   ├── pages/
│   │   │   ├── Login.jsx       # Authentication page
│   │   │   ├── Dashboard.jsx   # Main dashboard
│   │   │   ├── UploadPolicy.jsx # Analysis interface
│   │   │   ├── reports.jsx     # Report history
│   │   │   └── analytics.jsx   # Analytics view
│   │   ├── components/
│   │   │   ├── Navbar.jsx      # Navigation bar
│   │   │   └── Sidebar.jsx     # Sidebar menu
│   │   └── services/
│   │       └── api.js          # API integration
│
├── data/
│   └── dpdp_clauses.json       # DPDP Act 2023 clauses
│
├── docker-compose.yml          # Multi-container orchestration
├── Jenkinsfile                 # CI/CD pipeline
└── README.md                   # This file
```

---

## DPDP Act 2023 Compliance Clauses 📋

The system analyzes compliance with 5 key DPDP clauses:

| Clause | Section | Category | Description |
|--------|---------|----------|-------------|
| Notice Requirement | Section 5 | Transparency | Clear notice before data collection |
| Consent | Section 6 | Consent | Free, informed, specific consent required |
| Data Principal Rights | Section 11 | Rights | Access, correct, update, erase data |
| Data Security Safeguards | Section 8 | Security | Implement reasonable security measures |
| Grievance Redressal | Section 13 | Governance | Establish complaint resolution mechanism |

---

## Installation & Setup 🚀

### Prerequisites
- Python 3.8+
- Node.js 18+
- Docker & Docker Compose
- Git

### Quick Start (Development Mode)

#### 1. Clone Repository
```bash
git clone https://github.com/lokeshreddy47/dpdp-compliance-checker.git
cd dpdp-compliance-checker
```

#### 2. Setup Backend
```bash
cd dpdp-backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend will be available at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

#### 3. Setup Frontend
```bash
cd dpdp-frontend
npm install
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

## Docker Deployment 🐳

### Run Entire Stack with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build backend container (port 8000)
- Build frontend container (port 5173)
- Start both services automatically

Access:
- Frontend: **http://localhost:5173**
- Backend: **http://localhost:8000/docs**

### Stop Containers
```bash
docker-compose down
```

---

## Jenkins CI/CD Pipeline 🔄

The project includes automated deployment via Jenkins.

### Pipeline Stages:
1. **Build Docker Image**: Builds containers from docker-compose
2. **Run Containers**: Deploys containers automatically

### Jenkins Setup:
```bash
# Jenkins typically runs on port 8080
http://localhost:8080
```

### GitHub Integration:
- Webhooks configured for automatic builds on push
- Pipeline executes: Build → Deploy

---

## API Endpoints 📡

### Analysis Endpoints

**POST `/analyze-policy` (Main API)**
- Upload privacy policy file for analysis
- Response includes: compliance score, risk level, missing clauses, recommendations

**POST `/analyze-url`**
- Analyze privacy policy from website URL
- Automatically fetches and analyzes policy content

**POST `/check-compliance/`** (Advanced)
- Fetch website privacy policy
- Run AI analysis
- Generate PDF report
- Save to database

**GET `/download-report`**
- Download last generated PDF compliance report

**GET `/reports-history`**
- Retrieve history of all analyzed policies

### Response Format
```json
{
  "overall_score": 78.5,
  "risk_level": "Low Risk",
  "section_analysis": {
    "Notice Requirement": {
      "status": "Matched",
      "similarity_score": 92.3
    }
  },
  "missing_clauses": ["Data Security Safeguards"],
  "recommendations": [
    "The privacy policy should include a section for 'Data Security Safeguards'..."
  ],
  "graph_path": "reports/compliance_chart.png"
}
```

---

## AI Semantic Analysis 🤖

### How It Works:

1. **Policy Text Processing**: Extract and clean policy content
2. **Sentence Tokenization**: Break policy into meaningful sentences
3. **Semantic Embedding**: Convert sentences to numerical vectors using Sentence Transformers
4. **Similarity Matching**: Compare policy text against DPDP clause embeddings
5. **Scoring**: Calculate cosine similarity scores (0-100%)
6. **Threshold Classification**: Mark clauses as Matched/Missing based on similarity threshold
7. **Report Generation**: Create comprehensive compliance report

### Model Details:
- **Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **Similarity Threshold**: Configurable (default: 30%)
- **Processing**: Real-time analysis, no external API calls

---

## Demo Flow 🎬

### Step 1: Start System
```bash
# Terminal 1: Backend
cd dpdp-backend
python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd dpdp-frontend
npm run dev
```

### Step 2: Access Application
- Open browser: **http://localhost:5173**
- Backend Docs: **http://localhost:8000/docs**

### Step 3: Test Functionality
1. Upload a privacy policy file or enter a website URL
2. View compliance score and risk level
3. Download PDF report
4. View compliance chart

### Step 4: Show Docker Setup
```bash
docker-compose up --build
```

### Step 5: Expose with ngrok (Optional)
```bash
ngrok http 8000
```

This gives you a public HTTPS URL to your backend!

---

## Performance & Scalability ⚡

- **Real-time Analysis**: Analysis completes in <5 seconds
- **Database Optimization**: Indexed queries for history retrieval
- **Caching**: Report charts cached for performance
- **Containerization**: Scalable via container orchestration
- **Stateless API**: Supports horizontal scaling

---

## Future Enhancements 🔮

- [ ] JWT Authentication & Authorization
- [ ] Multi-language policy support
- [ ] Batch processing for multiple policies
- [ ] Email notification system
- [ ] Advanced analytics dashboard
- [ ] Policy comparison tools
- [ ] Machine learning model fine-tuning
- [ ] Mobile app support

---

## Testing 🧪

```bash
# Backend tests
cd dpdp-backend
pytest

# Frontend tests
cd dpdp-frontend
npm test

# Lint check
npm run lint
```

---

## Troubleshooting 🔧

### Backend won't start
```bash
# Ensure Python venv is activated
python --version  # Should show 3.x

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend port already in use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5173   # Windows
```

### Docker issues
```bash
# Clean up old containers
docker-compose down -v

# Rebuild from scratch
docker-compose up --build --no-cache
```

---

## Contributors 👨‍💻

- **Lokesh Reddy** - Full Stack Developer

---

## License 📄

This project is provided as-is for educational purposes.

---

## Contact & Support 📧

- GitHub: [lokeshreddy47/dpdp-compliance-checker](https://github.com/lokeshreddy47/dpdp-compliance-checker)
- Issues: Report bugs via GitHub Issues

---

**Made with ❤️ for DPDP Act 2023 Compliance**
