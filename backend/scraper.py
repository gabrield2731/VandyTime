from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

print("Starting scraper...")

url = "https://www.vanderbilt.edu/catalogs/kuali/undergraduate-24-25.php#/courses"
driver = webdriver.Chrome()
driver.get(url)
print("Opened browser")
# Getting dropdown buttons
buttons = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.md-btn.md-btn--icon.md-pointer--hover.md-inline-block.style__collapseButton___12yNL'))
)

for button in buttons:
    button.click()
    time.sleep(0.3)

course_links = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="#/courses/"]'))
)
cs_course_links = [link for link in course_links if link.text.startswith("CS")]
print("number of course links", len(course_links))
print("number of cs course links", len(cs_course_links))

for link in course_links:
        print(link)
        course_name = link.text.strip()
        course_link = link.get_attribute('href')
        # Open link in new tab
        driver.execute_script("window.open(arguments[0]);", course_link)
        driver.switch_to.window(driver.window_handles[1])

        try:
            course_description = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.course-view__pre___2VF54 > div'))
            ).text
        except Exception as e:
            print(f"Failed to load course description for {course_name}: {str(e)}")
            course_description = "Description not available"

        # Split course name by first '-', then get rid of leading/trailing whitespace
        course_code, course_name = course_name.split('-', 1)
        course_code = course_code.strip()
        course_name = course_name.strip()
        print(course_name)
        print(course_description)

        # Going back to main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()