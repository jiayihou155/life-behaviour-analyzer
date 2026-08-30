# Personal Life Multi‑Dimensional Behavior Tracker (CLI) v1.1

A robust, Python‑based self‑quantification system designed to log, track, and analyze individual daily behaviors across four core dimensions: Study, Sleep, Mood, and Expense.

## 🌟 Key Features
- **User Authentication & Security**: User registration and login protected with **SHA‑256 password hashing**.
- **Multi‑Module Behavior Logging**:
  - 📚 **Study**: Duration tracking, subject tagging, and custom notes.
  - 😴 **Sleep**: Bedtime, wake time, and daily sleep quality ratings (1–5).
  - 💛 **Mood**: Daily emotional state scores (1–5) and journal notes.
  - 💰 **Expense**: Transaction amounts, categories, and spending details.
- **Robustness & Validation**:
  - Strictly enforces `YYYY‑MM‑DD` date formatting and rating score ranges.
  - Exception handling for invalid numerical inputs to prevent runtime crashes.
  - Built‑in text length constraints to prevent unexpected input overflows.
- **Logging & Isolated Storage**:
  - Automatically manages user data, logs, and generated reports within an isolated `data/` directory.
  - Operational logs recorded via Python's standard `logging` module.
- **Automated Data Analysis**: Generates comprehensive review reports in Markdown format powered by `pandas`.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Data Analysis**: Pandas
- **Storage**: JSON (Locally stored with user data separation)
- **Security & Utilities**: Hashlib (SHA‑256), Datetime, Logging

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/jiayihou155/life‑behaviour‑analyzer.git
cd life‑behaviour‑analyzer
```
2. **Install dependencies**
```bash
pip install pandas
```
3. **Run the application**
```bash
python life_analyzer.py
```
## 📈 Project Roadmap
- [x] v1.0：Basic CLI functions, four‑dimension record‑keeping and markdown report generation.
- [x] v1.1 (Current): Date validation, SHA‑256 password hash, independent data directory, logging module, text‑length limit.
- [ ] v1.2 (Planned): Further optimize business logic.
- [ ] v2.0 (Planned): Migrate local JSON storage to a relational database (PostgreSQL / SQLite) for optimized multi‑user query performance.
- [ ] v3.0 (Planned): Build interactive data visualization dashboards using Matplotlib / Seaborn.
- [ ] v4.0 (Planned): Refactor backend into RESTful APIs using FastAPI with a modern Web frontend.




