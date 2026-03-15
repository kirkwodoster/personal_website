import streamlit as st
import numpy as np
import time
from pathlib import Path
import pandas as pd
from tools import inputs, utility, visual, clients, log_output
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

figuredata = Path(__file__).parent.parent.parent.parent / "data" / "figuredata.json"
kalshi_logo = Path(__file__).parent.parent.parent.parent / "assets" / "kalshi_logo.jpg"
nws_logo = Path(__file__).parent.parent.parent.parent / "assets" / "NWS_logo.png"
rect_logo = Path(__file__).parent.parent.parent.parent / "assets" / "logo_recrtangle.png"

def main_layout():
    
    st.set_page_config(
                       layout='wide',
                       page_title='Algo Weather Trading App'
                       )
    

    with st.container():
        col1, col2 = st.columns([1,10])
        
        with col1:
            with st.container():
                st.image(kalshi_logo, width=100)
            with st.container():
                st.image(nws_logo, width=100)
        
        with col2:
            st.header("Algorithmic Temperature Trading Bot")
            
            st.markdown(
                """
                <ul style='font-size: 20px;'>
                    <li>End-to-End Quantitative Trading Engine: Developed a fully autonomous Python-based system to trade weather derivatives on the Kalshi exchange.</li>
                    <li>Automated Data Pipeline: Engineered a robust ETL pipeline to scrape, sanitize, and aggregate multi-source geospatial temperature data.</li>
                    <li>Predictive Modeling: Implemented advanced statistical forecasting models to generate high-accuracy price signals for 6 major metropolitan markets.</li>
                    <li>API Integration & Execution: Built a low-latency execution layer using the Kalshi API for automated order management and risk mitigation without manual intervention.</li>
                </ul>
                """,
                unsafe_allow_html=True
            )
            
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([1,3],border=False, vertical_alignment='top')
        
        with col1:
            with st.container(border=True, gap=None,): #horizontal_alignment='center',vertical_alignment='center'):
                visual.account_balance_chart_card()
        with col2:
            with st.container(border=False, vertical_alignment='top'):
                visual.temp_chart1()
    
    with st.container(border=False,):
        col1, col2 = st.columns([.45,.55], border=False,)
        with col1:
            st.header('Open Trades')
        with col2:
            st.header('Historic Trades')
    with st.container(border=False,):
        col1, col2 = st.columns([.45,.55], border=False,)
        with col1:

            utility.position_data_chart()
        with col2:
            with st.container(border=False, gap=None, height=219):
                utility.portfolio_history()
    
    with st.container(border=False):
        st.header('Statistics')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                pie_chart_distrubtion = visual.pie_trade_counts(figuredata)
                st.plotly_chart(pie_chart_distrubtion,config={'displayModeBar': False})
        with col2:
            with st.container(border=True):
                barchart_total_profit_trades = visual.bar_chart_profit(figuredata)
                st.plotly_chart(barchart_total_profit_trades,config={'displayModeBar': False})
        with col3:
            with st.container(border=True):
                barchart_total_return_h = visual.bar_chart_total_return(figuredata)
                st.plotly_chart(barchart_total_return_h,config={'displayModeBar': False})
    with st.container(border=False):
        st.header('Server')        
    with st.container(height=300, border=True):
        # st.subheader('Model Log File', divider='green')
        model_log_file = log_output.model_output()
      
        st.text(model_log_file)

            
        # pass


        
if __name__ == "__main__":
    main_layout()