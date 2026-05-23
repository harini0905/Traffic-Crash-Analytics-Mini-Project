# Traffic Crash Analytics & Safety Intelligence Platform

## Project Description

This project analyzes traffic crash data using SQL and Python.  
The system uses SQLite as the database and Streamlit to build an interactive dashboard for traffic crash analysis.

The project helps identify:

- Crash trends
- Injury patterns
- High-risk streets
- Weather impact on crashes
- Dangerous time slots
- Hotspot zones

Interactive visualizations and advanced SQL queries are used to generate meaningful business insights.

---

# Features

- Traffic crash trend analysis
- Injury analysis dashboard
- Weather impact analysis
- High-risk street identification
- Crash hotspot zone analysis
- Interactive Streamlit dashboard

### Advanced SQL Concepts Used

- CTEs
- Window Functions
- Aggregations
- Ranking Functions

### Dynamic Filters

- Year
- Month
- Weather condition
- Street name

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data Analysis |
| SQL | Data Querying |
| SQLite | Database |
| Streamlit | Dashboard Development |
| Pandas | Data Manipulation |
| Matplotlib | Visualization |

---

# Project Structure

Project Structure:
TRAFFIC_CRASH_PROJECT/
│
├── app.py
├── README.md
├── traffic_crash.ipynb
├── traffic_crash.sqlite
├── Traffic_CrashesData.csv
├── traffic_crash.jpg
│
├── reports/
│   └── Traffic_Crash_Project_Report.pdf
│
└── screenshots/
    ├── Home Page 1.png
    ├── Home Page 2.png
    ├── Query Page.png
    ├── Visualisation 1.png
    └── Visualisation 2.png
  

---
## Dataset Notice

The original CSV dataset and SQLite database files have been excluded from the GitHub repository due to large file size limitations.

# How to Run the Project

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/TRAFFIC_CRASH PROJECT.git
```

## Step 2: Open the Project Folder

```bash
cd TRAFFIC_CRASH PROJECT
```

## Step 3: Run the Streamlit Application

```bash
streamlit run app.py
```

## Step 4: Open in Browser

After running the command, Streamlit will automatically open in your browser.

---

# Dashboard Screenshots

## Home Page 1

![Home Page 1](screenshots/Home%20Page%201.png)

## Home Page 2

![Home Page 2](screenshots/Home%20Page%202.png)

## Visualisation 1

![Visualisation 1](screenshots/Visualisation%201.png)

## Visualisation 2

![Visualisation 2](screenshots/Visualisation%202.png)

## Query Page

![Query Page](screenshots/Query%20Page.png)


---

# Business Insights Generated

- Identified dangerous weather and crash type combinations
- Found high-risk streets with maximum injuries
- Analyzed peak crash hours
- Detected dangerous time buckets
- Compared daylight vs darkness injury severity
- Identified hotspot crash zones using latitude and longitude

---

# Future Enhancements

- Machine Learning crash prediction
- Real-time traffic monitoring
- GIS map integration
- Cloud deployment
- Advanced forecasting models

---

# Author

## A. Harini

### Skills

- Python
- SQL
- Streamlit
- Data Analysis
- Pandas