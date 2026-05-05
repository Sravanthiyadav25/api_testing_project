# 🧪 Automated API Testing Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Pytest](https://img.shields.io/badge/Pytest-7.4.3-green?style=for-the-badge&logo=pytest)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey?style=for-the-badge&logo=flask)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4.0-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

### 🏆 First Prize — CSE Department Project Expo

*A complete automated API testing framework with a real-time web dashboard, live charts, and auto-generated HTML reports.*

</div>

---

## 📌 What is this?

This project is an **Automated API Testing Dashboard** that tests the **OpenWeatherMap REST API** using Python and Pytest. With a single click of the **"Run All Tests"** button, the system:

- Executes all **56 test cases** automatically
- Displays **real-time Pass/Fail results** with animated charts
- Generates a **detailed HTML report** showing every test case — its name, category, status, and execution time
- Updates the live dashboard instantly — no manual reporting needed

---

## 🎯 Testing Methodologies Covered

| # | Type | Tests | What it checks |
|---|------|-------|----------------|
| 🔵 | **Unit Testing** | 10 | Individual API response fields (status, temperature, humidity) |
| 🟢 | **Functional Testing** | 11 | End-to-end correct behavior for valid cities |
| 🔴 | **Negative Testing** | 10 | Error handling — wrong API key, invalid city, SQL injection |
| 🟡 | **Edge Case Testing** | 16 | Special characters, ALL CAPS, spaces, very long inputs |
| 🟣 | **Performance Testing** | 10 | Response time under 3 seconds, 10 concurrent requests |

> **Total: 56 automated test cases**

---

## ✨ Features

- 🖥️ **Real-time Dashboard** — Dark-themed professional UI with glassmorphism cards
- 📊 **Interactive Charts** — Live donut chart (Pass/Fail ratio) + bar chart (by category)
- 📄 **Auto-generated HTML Report** — Full test report generated instantly after every run
- 🔔 **Toast Notifications** — Success/failure alerts when tests complete
- 📱 **Responsive Design** — Works on mobile, tablet, and desktop
- 👤 **User Profile Sidebar** — Navigation menu with test suite breakdown and system status
- ⏱️ **Live Clock** — Real-time clock in the top bar
- 🔐 **Security Testing** — SQL injection and XSS prevention tests included

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Testing Framework | Pytest 7.4.3 |
| HTTP Requests | Requests 2.31.0 |
| Backend / Dashboard | Flask 3.0.0 |
| Frontend | HTML5 + CSS3 + JavaScript |
| Charts | Chart.js 4.4.0 |
| Icons | Bootstrap Icons |
| Fonts | Google Fonts (Space Grotesk, JetBrains Mono) |
| Report Generation | pytest-html 4.1.1 |
| API Under Test | OpenWeatherMap REST API |

---

## 📁 Project Structure

```
api_testing_project/
│
├── config/
│   └── config.py              # API key, base URL, settings
│
├── tests/
│   ├── test_unit.py           # 10 unit tests
│   ├── test_functional.py     # 11 functional tests
│   ├── test_negative.py       # 10 negative tests
│   ├── test_edge.py           # 16 edge case tests
│   └── test_performance.py    # 10 performance tests
│
├── utils/
│   └── api_helper.py          # Reusable API call functions
│
├── dashboard/
│   ├── app.py                 # Flask web dashboard (main server)
│   ├── templates/
│   │   ├── index.html         # Main dashboard UI
│   │   └── report.html        # Report viewer page
│   └── static/                # CSS and JS assets
│
├── reports/                   # Auto-generated HTML reports (after running tests)
├── requirements.txt           # All dependencies
└── README.md                  # This file
```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/api-testing-dashboard.git
cd api-testing-dashboard
```

### 2. Install dependencies
```bash
pip install pytest requests pytest-html flask pytest-timeout
```

### 3. Add your API key
Open `config/config.py` and replace:
```python
OPENWEATHERMAP_API_KEY = 'your_api_key_here'
```
Get a free API key at 👉 [openweathermap.org/api](https://openweathermap.org/api)

### 4. Start the dashboard
```bash
python dashboard/app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

### 6. Click "Run All Tests" 🎉
Watch all 56 tests execute in real-time!

---

## 📊 Dashboard Preview

```
┌─────────────────────────────────────────────────────┐
│  🧪 API Testing Dashboard                           │
│  ● System Ready                                     │
├──────────┬──────────┬──────────┬────────────────────┤
│ Total    │ Passed   │ Failed   │ Duration           │
│   56     │   11     │   45     │  18.3s             │
├──────────┴──────────┴──────────┴────────────────────┤
│  [▶ Run All Tests]  [📄 View Report]                │
├─────────────────────────┬───────────────────────────┤
│  🍩 Pass/Fail Chart     │  📊 Tests by Category     │
├─────────────────────────┴───────────────────────────┤
│  Latest Test Results Table (all 56 tests)           │
└─────────────────────────────────────────────────────┘
```

---

## 📄 Auto-Generated Report

After clicking **Run All Tests**, a full HTML report is automatically saved to `reports/report.html` containing:

- ✅ Total tests run
- ✅ Pass / Fail / Skip count per test
- ✅ Execution time per test case
- ✅ Error messages for failed tests
- ✅ Python environment details
- ✅ Timestamp of the test run

Click **"View Report"** on the dashboard to open it instantly!

---

## ⚠️ About Failed Tests

> The 45 failed tests are **intentional and expected.**

Our **negative tests** and **edge case tests** are specifically designed to pass invalid inputs (wrong API keys, invalid city names, SQL injection strings) to the API. When these tests **fail**, it means our framework **successfully detected** the error — which is exactly what a testing framework is supposed to do! ✅

---

## 👩‍💻 Author

**G. Sravanthi Yadav**
CSE Department · Project Expo 2026 🏆 First Prize

---

## 📜 License

This project is licensed under the MIT License.

---
Contributions are welcome! linkedin : https://www.linkedin.com/in/sravanthi-yadav-tech/ 
e-mail: sravanthiyadav348@gmail.com
<div align="center">
  <b>Built with ❤️ using Python, Pytest & Flask</b>
</div>
