# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException

from bs4 import BeautifulSoup
import json

from flask import Flask, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "7C1C5919-13B0-47AC-B873-9EB53114964F"
jwt = JWTManager(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify("Ok")

@app.errorhandler(404)
def not_found_error(error):
    return jsonify('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error.message), 500

# Offshore Leaks

@app.route('/offshore', methods=['POST'])
@cross_origin()
#@jwt_required()
def get_offshore_leaks():

    # Get Data from Url
    options = webdriver.ChromeOptions()
    # To Debug
    #options.add_experimental_option("detach", True)

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://offshoreleaks.icij.org/")
        driver.implicitly_wait(10)

        driver.find_element(By.XPATH, '//*[@id="accept"]').click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__BVID__73___BV_modal_body_"]/form/div/div[2]/button'))).click()

        searchBar = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/form/input[1]')
        data = json.loads(request.data)
        searchBar.send_keys(data['name'])
        searchBar.send_keys(Keys.ENTER)

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search_results"]/div[1]/table'))).get_attribute("class")

        response = driver.page_source
        driver.quit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')

        # Find Tables
        table = soup.find('table', {"class": "table table-sm table-striped search__results__table"})
        tbody = table.find_all('tbody')

        # Iterate Over Tables
        foundRows = []
        for table in tbody:
            for tr in table.find_all('tr'):
                row = tr.find_all('td')
                obj = {
                    "entity": row[0].find('a').text.strip(),
                    "jurisdiction": row[1].text.strip(),
                    "linkedTo": row[2].text.strip(),
                    "dataFrom": row[3].find('a').text.strip()
                }
                foundRows.append(obj)

        # Return Response
        respObj = {
            "hits": len(foundRows),
            "rows": foundRows,
            "message": "Ok"
        }
        return jsonify(respObj)

    except:
        # Return Error
        respObj = {
            "hits": 0,
            "rows": [],
            "message": 'Could not find any results'
        }
        return jsonify(respObj), 405



# World Bank

@app.route('/world', methods=['POST'])
@cross_origin()
#@jwt_required()
def get_world_bank():

    # Get Data from Url
    options = webdriver.ChromeOptions()
    # To Debug
    #options.add_experimental_option("detach", True)
    
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms")
        driver.implicitly_wait(10)

        driver.find_element(By.XPATH, '//*[@id="teaser-2ad0826d34"]/button').click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="k-debarred-firms"]/div[3]/table'))).click()
        searchBar = driver.find_element(By.ID, 'category')
        data = json.loads(request.data)
        searchBar.send_keys(data['name'])
        searchBar.send_keys(Keys.ENTER)

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="k-debarred-firms"]/div[3]/table'))).get_attribute("class")

        response = driver.page_source
        driver.quit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')

        # Find Table
        table = soup.find_all('table', {'role': 'grid'})
        tbody = table[1].find('tbody')

        # Iterate Over Elements In Table
        foundRows = []
        for tr in tbody.find_all('tr'):
            row = tr.find_all('td')
            obj = {
                "firmName": row[0].text,
                "address": row[2].text,
                "country": row[3].text,
                "formDate": row[4].text,
                "toDate": row[5].text,
                "grounds": row[6].text
            }
            foundRows.append(obj)

        # Return Response
        respObj = {
            "hits": len(foundRows),
            "rows": foundRows,
            "message": "Ok"
        }
        return jsonify(respObj)

    except:
        # Return Error
        respObj = {
            "hits": 0,
            "rows": [],
            "message": "Could not find any results"
        }
        return jsonify(respObj), 405



# Sanctions List

@app.route('/sanctions', methods=['POST'])
@cross_origin()
#@jwt_required()
def get_sanctions_list():

    # Get Data from Url
    options = webdriver.ChromeOptions()
    # To Debug
    #options.add_experimental_option("detach", True)
    
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://sanctionssearch.ofac.treas.gov/Default.aspx")
        driver.implicitly_wait(10)

        minScore = driver.find_element(By.NAME, 'ctl00$MainContent$Slider1_Boundcontrol')
        minScore.send_keys(Keys.CONTROL + "a")
        minScore.send_keys(Keys.DELETE)
        minScore.send_keys("80")

        searchBar = driver.find_element(By.NAME, 'ctl00$MainContent$txtLastName')
        data = json.loads(request.data)
        searchBar.send_keys(data['name'])
        searchBar.send_keys(Keys.ENTER)

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'gvSearchResults'))).get_attribute("class")

        response = driver.page_source
        driver.quit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')

        # Find Table
        table = soup.find(id='gvSearchResults')

        # Iterate Over Elements In Table
        foundRows = []
        for tr in table.find_all('tr'):
            row = tr.find_all('td')
            obj = {
                "name": row[0].find('a').text,
                "address": row[1].text,
                "type": row[2].text,
                "Program": row[3].text,
                "List": row[4].text,
                "score": row[5].text
            }
            foundRows.append(obj)

        # Return Response
        respObj = {
            "hits": len(foundRows),
            "rows": foundRows,
            "message": "Ok"
        }
        return jsonify(respObj)

    except:
        # Return Error
        respObj = {
            "hits": 0,
            "rows": [],
            "message": "Could not find any results"
        }
        return jsonify(respObj), 405


if __name__ == '__main__':
    app.run(debug = True)
