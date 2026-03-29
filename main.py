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
        st.Page('pages/projects/crypto/crypto.py', title='Crypto Trading Bot'),
        ]
        }

pg = st.navigation(pages, position='top', expanded=True,)

if __name__ == '__main__':

    pg.run()



