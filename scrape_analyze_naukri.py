import sys
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------------- STEP 0: Job Role from User Input ----------------------
job_role = sys.argv[1] if len(sys.argv) > 1 else "data-analyst"
search_url = f"https://www.naukri.com/{job_role}-jobs"

# ---------------------- STEP 1: Selenium Setup ----------------------
service = Service("C:/Users/Dell/Downloads/chromedriver-win64/chromedriver.exe")  # ✅ Adjust if needed
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

driver.get(search_url)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

jobs = driver.find_elements(By.CSS_SELECTOR, "div.cust-job-tuple.layout-wrapper")

job_titles, companies, locations, links, descriptions, salaries = [], [], [], [], [], []

# ---------------------- STEP 2: Loop through each job ----------------------
for job in jobs:
    try:
        title = job.find_element(By.CSS_SELECTOR, "a.title").text.strip()
        company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text.strip()
        location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text.strip()
        link = job.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")

        # Open job link to get description & salary
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        try:
            desc = driver.find_element(By.CSS_SELECTOR, "div.styles_JDC__dang-inner-html__h0K4t").text.strip()
        except:
            desc = "Not Found"

        try:
            salary_elem = driver.find_element(By.XPATH, '//span[contains(text(),"₹") or contains(text(),"LPA") or contains(text(),"lakh") or contains(text(),"per annum")]')
            salary_text = salary_elem.text.strip()
        except:
            salary_text = "Not Mentioned"

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # ✅ Append only after success
        job_titles.append(title)
        companies.append(company)
        locations.append(location)
        links.append(link)
        descriptions.append(desc)
        salaries.append(salary_text)

        print(f"✅ {title} | {company} | {salary_text}")

    except Exception as e:
        print("❌ Skipping one job due to error:", e)
        try:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        continue

driver.quit()

# ---------------------- STEP 3: Create DataFrame ----------------------
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": companies,
    "Location": locations,
    "Link": links,
    "Description": descriptions,
    "Salary": salaries
})

df.to_csv("naukri_jobs_with_descriptions.csv", index=False)
print("✅ Scraped job data saved to 'naukri_jobs_with_descriptions.csv'")

# ---------------------- STEP 4: Clean Descriptions ----------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)      # Remove numbers
    return text

df['Clean_Description'] = df['Description'].apply(clean_text)

# ---------------------- STEP 5: Extract Skills ----------------------
skills_list = [
    'python', 'sql', 'excel', 'power bi', 'tableau', 'machine learning', 'deep learning',
    'data visualization', 'statistics', 'analytics', 'pandas', 'numpy',
    'nlp', 'matplotlib', 'seaborn', 'dash', 'scikit-learn', 'big data', 'aws'
]

def extract_skills(text):
    return [skill for skill in skills_list if skill in text]

df['Skills'] = df['Clean_Description'].apply(extract_skills)

# ---------------------- STEP 6: Extract Salary with Regex ----------------------
def extract_salary(text):
    text = str(text).lower().strip()
    text = text.replace('₹', 'rs.').replace('p.a.', 'pa').replace('per annum', 'pa')
    pattern = r'(?:rs\.?|₹)?\s?\d{1,3}(?:[,\d]{1,10})?\s?(?:lpa|lakhs?|pa|k|per\smonth)?'
    return re.findall(pattern, text)

# df['Salaries_Extracted'] = df['Salary'].apply(extract_salary)

# ---------------------- STEP 7: Location-wise Demand ----------------------
print("\n📍 Top Hiring Locations:")
print(df['Location'].value_counts().head(10))

# ---------------------- STEP 8: Top Skills ----------------------
all_skills = sum(df['Skills'], [])
skill_counts = Counter(all_skills)

print("\n💼 Top Skills in Demand:")
for skill, count in skill_counts.most_common(10):
    print(f"{skill.title()}: {count}")

# ---------------------- STEP 9: Save Cleaned Data ----------------------
df.to_csv("naukri_cleaned_jobs.csv", index=False)
print("\n✅ Cleaned data saved as 'naukri_cleaned_jobs.csv'.")

# ---------------------- STEP 10: Optional WordCloud ----------------------
try:
    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(" ".join(df['Clean_Description']))
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Most Common Words in Job Descriptions")
    plt.show()
except Exception as e:
    print("⚠️ WordCloud Error:", e)
