import pytz

# hour = 8

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