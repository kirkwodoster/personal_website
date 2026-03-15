import streamlit as st
import numpy as np
import time
from PIL import Image
from pathlib import Path
import pandas as pd
from tools import inputs, utility, visual, clients
from datetime import datetime
import plotly.graph_objects as go
import pprint
from datetime import datetime
import pytz
from tools import inputs, utility, visual
from tools.clients import client
# import pytz


pages = {
    "About Me": [
            st.Page('pages/about/about.py', title='About Corey')
            # st.Page('pages/about/resume.py', title='CV')
        ],
        "Personal Projects": [
        st.Page('pages/projects/weatheralgo/weatheralgo.py', title='Algo Trading Bot'),

        ]
        }

pg = st.navigation(pages, position='top', expanded=True,)

# st.html("""
# <style>
# .stAppHeader {
#     background-color:#023020;
# }
# </style>
# """)     

if __name__ == '__main__':
    
    # fees_dict = client.get_positions()['orders']

     
    # for j in fees_dict:
    #     fees_datetime = j.get('last_update_time')
    #     fees_date = fees_datetime.split('T')[0]
    #     fees = j.get('taker_fees')
    #     # fees_cents = (float(fees)) * -1
    #     # print(fees_dict)
    #     print(fees_dict)
        
        
        
    pg.run()



