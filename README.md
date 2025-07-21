# Job-Market-Trend-Analyzer
# Job Market Trend Analyzer (Python • SQL • Power BI)

This project helps analyze trends in the tech job market by extracting and visualizing job data from **Naukri.com** using web scraping and natural language processing (NLP). It provides insights into job roles, locations, skill demands, and more through a clean Power BI dashboard.

---

## 🔍 Features

- 🔎 **Web Scraping**: Collects 1,000+ job listings from Naukri.com using Selenium.
- 🧠 **NLP Analysis**: Extracts and analyzes top skills from job descriptions.
- 📊 **Interactive Power BI Dashboard**: Displays trends in demand by skill, location, salary range, and job title.
- 🗃️ **Data Cleaning & Export**: Outputs to `.csv` for easy analysis and dashboarding.

---

## 🧰 Tools & Technologies Used

- Python (Selenium, Pandas, NLTK)
- SQL (for querying cleaned data)
- Power BI (for visualizing trends)
- Git & GitHub (for version control and sharing)

---

## 📁 File Descriptions

| File Name                        | Description                                         |
|----------------------------------|-----------------------------------------------------|
| `scrape_analyze_naukri.py`       | Scrapes job data and performs initial processing   |
| `naukri_cleaned_jobs.csv`        | Cleaned dataset for dashboard use                  |
| `naukri_jobs_with_descriptions.csv` | Raw scraped job listings with full descriptions |
| `job_market.pbix`                | Power BI dashboard visualizing all insights        |
| `README.md`                      | Project documentation                              |

---

## 📊 Dashboard Preview

*(Add a screenshot named `dashboard.png` in a `/screenshots` folder and it will show here)*

```md
![Dashboard Preview](screenshots/dashboard.png)
