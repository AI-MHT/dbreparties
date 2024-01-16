from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set the path to your WebDriver executable (e.g., chromedriver or geckodriver)
# Download the appropriate driver for your browser: https://sites.google.com/chromium.org/driver/
driver_path = 'C:/Users/AI-MHT/Downloads/chromedriver_win32'

# Create a new instance of the browser driver (e.g., Chrome or Firefox)
driver = webdriver.Chrome(executable_path=driver_path)

# Open Oracle Live SQL website
driver.get('https://livesql.oracle.com/')

# Find and click on the "Sign In" button
sign_in_button = driver.find_element('link text', 'Sign In')
sign_in_button.click()

# Enter your Oracle Live SQL username and password
username_input = driver.find_element('id', 'username')
password_input = driver.find_element('id', 'password')

username_input.send_keys('aiman.mouhat.etu21@ensem.ac.ma')
password_input.send_keys('@Lol1234')

# Find and click on the "Sign In" button
login_button = driver.find_element('id', 'btn_login')
login_button.click()

# Wait for the login to complete (you might need to adjust the sleep time)
time.sleep(5)

# Find and select the SQL Worksheet tab
sql_worksheet_tab = driver.find_element('id', 'nav-sql-worksheet')
sql_worksheet_tab.click()

# Find the SQL query input area and send a SQL query
sql_input = driver.find_element('css selector', 'div.ace_content')
sql_input.send_keys('SELECT * FROM garage;')

# Find and click on the "Run Statement" button
run_button = driver.find_element('id', 'sqlworksheet-execution-button')
run_button.click()

# Wait for the query to execute (you might need to adjust the sleep time)
time.sleep(5)

# Capture and print the results
result_output = driver.find_element('id', 'sqlworksheet-results-panel')
print(result_output.text)

# Close the browser
driver.quit()
