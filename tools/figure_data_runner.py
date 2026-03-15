import numpy as np
import pandas as pd
from clients import client
from pathlib import Path
import time
import json



def history_of_returns():
    
    series_counts = {
    "KXHIGHDEN": [],
    "KXHIGHCHI": [],
    "KXHIGHMIA": [],
    "KXHIGHAUS": [],
    "KXHIGHPHIL":[],
    "KXHIGHLAX": []
                    }
    
    cursor =  None
   
    max_iterations = 0
    while max_iterations < 10:
        time.sleep(3)
        try:
            max_iterations += 1
            
            settlement_data = client.get_portfolio_settlements(cursor=cursor)
            
            for item in settlement_data.get('settlements'):
                
                ticker = item.get('ticker').split('-')[0]
                revenue = item.get('revenue')
                filled_cost = item.get('yes_total_cost')
                
                my_return = (revenue - filled_cost)/100
                
                series_counts[ticker].append(my_return)
                
            cursor =  settlement_data.get('cursor')
            
        except:
            pass
    figuredata = Path(__file__).parent.parent / "data" / "figuredata.json"
    with open(figuredata, 'w') as f:
         json.dump(series_counts, f, indent=4)
 

if __name__ == '__main__':

    history_of_returns()
    # figuredata = Path(__file__).parent.parent / "data" / "figuredata.csv"
    # print(temp_data)
#    /root/myenv/my_resume/tools