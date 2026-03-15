import pandas as pd
import numpy as np
import requests
from datetime import datetime
import logging
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
import time
import requests
import random
import pandas as pd
import time
import pytz
from pathlib import Path

def all_markets(hour=8):
    all_markets = {
                "DENVER": {
                    "SERIES": "KXHIGHDEN",
                    "TIMEZONE": pytz.timezone("America/Denver"),
                    "ICAO": "KDEN",
                    "URL": f"https://www.weather.gov/wrh/timeseries?site=KDEN&hours={hour}",
                    "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=39.8589&lon=-104.6733&FcstType=digitalDWML",
                
                },
                "CHICAGO": {
                    "SERIES": "KXHIGHCHI",
                    "TIMEZONE": pytz.timezone("America/Chicago"),
                    "ICAO": "KMDW",
                    "URL": f"https://www.weather.gov/wrh/timeseries?site=KMDW&hours={hour}",
                    "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=41.7842&lon=-87.7553&FcstType=digitalDWML",
                    
                },
                "MIAMI": {
                    "SERIES": "KXHIGHMIA",
                    "TIMEZONE":  pytz.timezone("US/Eastern"),
                    "ICAO": "KMIA",
                    "URL": f"https://www.weather.gov/wrh/timeseries?site=KMIA&hours={hour}",
                    "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=25.7934&lon=-80.2901&FcstType=digitalDWML",
                
                },
                "AUSTIN": {
                    "SERIES": "KXHIGHAUS",
                    "TIMEZONE":  pytz.timezone("US/Central"),
                    "ICAO": "KAUS",
                    "URL": f"https://www.weather.gov/wrh/timeseries?site=KAUS&hours={hour}",
                    "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=30.1945&lon=-97.6699&FcstType=digitalDWML",
                
                },
                "PHILADELPHIA": {
                    "SERIES": "KXHIGHPHIL",
                    "TIMEZONE":  pytz.timezone("US/Eastern"),
                    "ICAO": "KPHL",
                    "URL": f"https://www.weather.gov/wrh/timeseries?site=KPHL&hours={hour}",
                    "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=39.8721&lon=-75.2407&FcstType=digitalDWML",
                    
                },
                "LOS ANGELES": {
                    "SERIES":"KXHIGHLAX",
                    "TIMEZONE":  pytz.timezone("America/Los_Angeles"),
                    "ICAO": "KLAX",
                    "URL": f"https://www.weather.gov/wrh/timeseries?site=KLAX&hours={hour}",
                    "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=33.9425&lon=-118.409&FcstType=digitalDWML",
                    
                }
            }

    return all_markets

series_city = {
    "KXHIGHDEN": 'Denver',
    "KXHIGHCHI": 'Chicago',
    "KXHIGHMIA": 'Miami',
    "KXHIGHAUS": 'Austin',
    "KXHIGHPHIL": 'Philidelphia',
    "KXHIGHLAX": 'Los Angeles'
}


logging.getLogger('seleniumwire').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('webdriver_manager').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)



def logging_settings():
      
    return logging.basicConfig(
    level=logging.CRITICAL,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log format
    handlers=[logging.StreamHandler()]  # Output logs to the terminal
)

logging_settings()



USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)


def rand_proxy_api():
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25",
        headers={"Authorization": "Token 79swcqtwfm1c3k3huotc48v128dyevosunyqyl9u"}
    )
    proxy_list = response.json()['results']

    rand_proxy_list = random.choice(proxy_list)
    username = rand_proxy_list['username']
    password = rand_proxy_list['password']
    proxy = rand_proxy_list['proxy_address']
    port = rand_proxy_list['port']
    
    server = f'http://{proxy}:{port}'
    
    return {'server': server, 'username': username, 'password': password}


def scrape_nws(url):
    random_proxy = rand_proxy_api()
    random_user_agent =  get_random_user_agent()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            proxy={
                                    'server': random_proxy['server'],
                                    'username': random_proxy['username'],
                                    'password': random_proxy['password']
                                    },
                                    headless=True)  # Set headless=True for background execution
        
        context = browser.new_context(
        user_agent= random_user_agent,
        viewport={'width': 1920, 'height': 1080}, # Set a common viewport size
        # locale="en-US" # Set a common locale
             )
        page = context.new_page()
        page.goto(url)

        try:
           
            #Dew Point Button
            page.wait_for_selector("button[aria-label='Show Dew Point']").click()
            # Humidity Button
            page.wait_for_selector("button[aria-label='Show Relative Humidity']").click()
            #Chart Button
            page.wait_for_selector("button[aria-label='View chart menu, Chart']").click()
            #View Table
            page.wait_for_selector("li.highcharts-menu-item:has-text('View data table')").click()
            #Table
            table = page.wait_for_selector('xpath=//table[@summary="Table representation of chart."]')
            rows = table.query_selector_all('tbody tr')


            data = {
                'Temp': [],
                'Datetime': []
                    }
            
            for row in rows:
                temp = row.query_selector('td').inner_text().strip()
                datetime = row.query_selector('th').inner_text().strip()

                data['Temp'].append(temp)
                data['Datetime'].append(datetime)
                
            scraped_df = pd.DataFrame(data)
            scraped_df['Temp'] = scraped_df['Temp'].astype(float)
            scraped_df['Datetime'] = pd.to_datetime(scraped_df['Datetime'])
            
            browser.close()

            temp = scraped_df['Temp']
            datetime = scraped_df['Datetime']
            # print(f'Temp: {temp[0]}, Datetime: {datetime[0]}')
            return temp, datetime
                
        except Exception as e:
            print(f"NWS Scrape: {e}")

        finally:
            browser.close()            

            
def scrape_to_csv():
    

    all_market_dict = all_markets()
        
    df_dict = []
    for loc in all_market_dict:
            time.sleep(60)
        
            location = loc
            series = all_market_dict[loc].get("SERIES")
            
            timezone = all_market_dict[loc].get("TIMEZONE")
            print(f'--- {location} ---')
            current_hour = datetime.now(timezone).hour + 1
            # current_hour = 8
            all_market_dict = all_markets(hour=current_hour)
            url = all_market_dict[loc].get("URL")
            
            # st.subheader(f'{series}')
            # data = fetch_temp_data(url)
        
            data = scrape_nws(url)
            # data = [np.linspace(1,5,5), pd.date_range(start='2025-01-06', periods=5, freq='D')]  # Modified to make dummy data different
           
            df = pd.DataFrame({"Temperature": data[0], "Date Time": data[1], "Location": location})
            # print(df)
            current_day = datetime.now(timezone).day
            df = df[df['Date Time'].dt.day == current_day]
            
            df_dict.append(df)
            
    
    df_concat = pd.concat(df_dict)

    temp_to_disc_csv  = Path(__file__).parent.parent / "data" / 'temp_data.csv'
    df_concat.to_csv(temp_to_disc_csv)
    
if __name__ == '__main__':
    scrape_to_csv()