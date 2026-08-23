# RetailPulse AI — Developer & Contribution Guide

This guide describes how to set up, run, test, and contribute to the RetailPulse AI codebase.

---

## 1. Prerequisites

- **Python 3.10+** (Python 3.14 compatible)
- **Node.js 18+** & **npm**
- **Git**
- Optional: PostgreSQL (SQLite default requires zero external database installation)

---

## 2. Environment Setup

### Backend & Analytics Setup
```powershell
# Clone or navigate to the repository
cd retailpulse-ai

# Create and activate virtual environment (optional)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### Frontend Setup
```powershell
cd frontend
npm install
```

---

## 3. Database Seeding & Model Training

Execute the end-to-end data pipeline from the repository root:
```powershell
# 1. Generate 57k+ synthetic orders across 12k customers
python scripts/generate_data.py

# 2. Initialize database schema & bulk load data
python database/init_db.py

# 3. Train RFM Segmentation, Churn Classification, and Demand Forecasting models
python scripts/train_models.py

# 4. Export Power BI and Tableau datasets
python scripts/export_bi_datasets.py
```

---

## 4. Running the Applications

### Start the FastAPI Backend Server
```powershell
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at `http://localhost:8000/docs`.

### Start the React Frontend Development Server
```powershell
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 5. Running Automated Tests

Run the full pytest suite:
```powershell
pytest backend/tests/ -v
```

Run frontend typecheck and build validation:
```powershell
cd frontend
npm run build
```
