import streamlit as st
import numpy as np
import pandas as pd
from tools import inputs, utility
from tools.clients import client
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import time
from pathlib import Path
from plotly.subplots import make_subplots
import base64
import json

#https://colorhunt.co/palette/070f2b1b1a55535c919290c3

def get_data_from_csv():
    temp_data = Path(__file__).parent.parent / "data" / "temp_data.csv"
    df = pd.read_csv(temp_data)
    df = df[['Temperature', 'Date Time','Location']]
    
    return df


def temp_chart1():
    
    def temp_chart_build(num,city):
        fig = go.Figure()
        fig.add_trace(
                go.Scatter(
                    x=df['Date Time'].values,
                    y=df['Temperature'].values,
                    # line=dict(color=colors[num]),
                    name=city
                          
                ),
            ),
            # This layout makes the charts look good inside columns
        fig.update_traces(line_color='#FFE135')
        fig.update_yaxes(fixedrange=True)
        fig.update_xaxes(fixedrange=True)
        fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=157,
                    margin={'t':30, 'l':10, 'b':10, 'r':10}, # Added top margin for title
                    showlegend=False,
        )
        return st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False}
            )
    
    all_market_dict = inputs.all_markets()
    
    cities = list(all_market_dict.keys())
    # columns = st.columns(len(cities), border=True)
    

    row1_col = st.columns(3, border=True, vertical_alignment='top')
    # st.write("") # Add some space between rows
    row2_col = st.columns(3, border=True, vertical_alignment='top')
    
    for num, city in enumerate(cities):
        
        df = get_data_from_csv()
        df = df[df['Location'] == city]
        
        denver = Path(__file__).parent.parent / "assets" / "denver.png"
        chicago = Path(__file__).parent.parent / "assets" / "chicago.png"
        miami = Path(__file__).parent.parent / "assets" / "miami.png"
        austin = Path(__file__).parent.parent / "assets" / "austin.png"
        philadelphia = Path(__file__).parent.parent / "assets" / "philadelphia.png"
        los_angeles = Path(__file__).parent.parent / "assets" / "los_angeles.png"
        image_list = [denver, chicago, miami, austin, philadelphia, los_angeles]
        
        if num < 3:    
            with st.container(vertical_alignment='top'):
                with row1_col[num]:
                    inner_col1, inner_col2 = st.columns([.3,.7], vertical_alignment='center')
                    with inner_col1:
                        
                        st.markdown(
                    f"""    
                        <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                        <span style="margin: 0; white-space: nowrap; font-size: 16px">{city}</span>
                        </div>
                        """,
                    unsafe_allow_html=True,
                )   
                        st.write(" ")
                        st.image(image=image_list[num], width=125)
                    with inner_col2:
                        temp_chart_build(num=num,city=city)
 
        else:
            with st.container(vertical_alignment='top'):
                with row2_col[num-3]:
                    
                    inner_col1, inner_col2 = st.columns([.3,.7], vertical_alignment='center')
                    with inner_col1:
                                            
                        st.markdown(
                        f"""    
                        <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                        <span style="margin: 0; white-space: nowrap; font-size: 16px">{city}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                        )
                        st.write(" ")
                        st.image(image=image_list[num],width=125)
                    
                    with inner_col2:
                        temp_chart_build(num=image_list[num],city=city)
                    
                    # temp_chart_build(num=num,city=city)
        
                
                
def account_balance_chart_card1():
    
    dollar_sign = Path(__file__).parent.parent / "assets" / "dollar_sign.png"

    with st.container():
        date_balances = utility.historical_balances()
        # dates = date_balances.keys()
        balances = date_balances.values()
        balance = client.get_balance()['balance']/100
        # st.header(f'{balance}')
        # st.image(f'{dollar_sign}', width=50)
        st.markdown(
                    """
                    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                        <img src="data:image/png;base64,{0}" width="50">
                        <span style="margin: 0; white-space: nowrap; font-size: 20px">Account Balance: ${1:,.2f}</span>
                    </div>
                    <br>
                    """.format(
                        base64.b64encode(open(dollar_sign, "rb").read()).decode(),
                        balance
                    ),
                    unsafe_allow_html=True,
                )
    with st.container():
        pass

            
def account_balance_chart_card():
    
    # col1, col2 = st.columns([1,3], border=True)
    dollar_sign = Path(__file__).parent.parent / "assets" / "dollar_sign.png"

    # C:\Users\corey\Documents\python\streamlit\my_resume\assets\dollar_sign.png
    date_balances = utility.historical_balances()
    dates = date_balances.keys()
    balances = date_balances.values()
    balance = client.get_balance()['balance']/100
    # st.header(f'{balance}')
    
    with st.container():
        # inner_col, = st.columns(1,gap=None, vertical_alignment="center")
        # with inner_col:
            # st.image(f'{dollar_sign}', width=50)
            st.markdown(
                            """
                            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                                <img src="data:image/png;base64,{0}" width="50">
                                <span style="margin: 0; white-space: nowrap; font-size: 20px">Account Balance: ${1:,.2f}</span>
                            </div>
                            <br>
                            """.format(
                                base64.b64encode(open(dollar_sign, "rb").read()).decode(),
                                balance
                            ),
                            unsafe_allow_html=True,
                        )

    with st.container():
        account_balance_chart()
            
def account_balance_chart():
    date_balances = utility.historical_balances()
    dates = date_balances.keys()
    balances = date_balances.values()
    balance = client.get_balance()['balance']/100
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(dates),
            y=list(balances),
            line=dict(color='#2ca02c',
                      width=2)
        )
    )
    
    fig.update_traces(line_color='#228B22')
    fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=300,
                    margin={'t':30, 'l':10, 'b':10, 'r':10}, # Added top margin for title
                    showlegend=False,
                    
                )
                
            # Hide axes for a cleaner "sparkline" look
    fig.update_xaxes(visible=True)
    fig.update_yaxes(visible=True)
    fig.update_yaxes(fixedrange=True)
    fig.update_xaxes(fixedrange=True)
            
    return st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False}
            )
    

def pie_chart_historic_trades():
    
    pie_chart_data = Path(__file__).parent.parent / "data" / "pie_chart_distribution.csv"
    df = pd.read_csv(pie_chart_data)
    values = df.values.reshape(1,6)[0]
        
    labels = list(inputs.series_city.values())
    
    irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                 'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
    
    fig = go.Figure(data=go.Pie(labels=labels, values=values, marker_colors=irises_colors))
    fig.update_traces(hoverinfo='label+percent  ', textinfo='label+percent')
    fig.update(layout_title_text='Distrubtion of Trades',layout_showlegend=False)
    
    return fig


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

    return series_counts
    

def pie_trade_counts(data):
    
    with open(data, 'r') as f:
    # 'r' means open the file in read mode
        loaded_data = json.load(f)
    
    returns = loaded_data
        
    for keys in returns.keys():
        returns[keys] = len(np.trim_zeros(returns[keys]))
        
    labels = list(inputs.series_city.values())
    values =  list(returns.values())
    irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                 'rgb(175, 49, 35)', 'rgb(36, 73, 147)', 'rgb(204, 121, 167)']
    
    fig = go.Figure(data=go.Pie(labels=labels, values=values, marker_colors=irises_colors, insidetextfont=dict(color='white')))
    fig.update_traces(hoverinfo='label+percent  ', textinfo='label+percent')
    fig.update(layout_title_text='Distrubtion of Trades',layout_showlegend=False)
    
    return fig

def bar_chart_profit(data):
    
    with open(data, 'r') as f:
    # 'r' means open the file in read mode
        loaded_data = json.load(f)
    
    returns = loaded_data

    
    for keys, values in zip(returns.keys(), returns.values()): 
      
        total_trades = len(np.trim_zeros(values))
        total_profit_trades = sum(1 for trade in values if trade > 0)
        returns[keys] = round(total_profit_trades / total_trades, 1)
        # df = pd.DataFrame(returns)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(returns.keys()),
        y=list(returns.values()),
        name='% Trades Profitable',
        marker_color='rgb(55, 83, 109)',
        
    ))

    # Update properties of the BARS (the trace)
    fig.update_traces(
        texttemplate='%{y:.0%}', # Format the text on the bars as a percentage
        textposition='outside'
    )

    # Update properties of the LAYOUT (title, axes, legend)
    fig.update_layout(
        title_text="Percent of Porfitable Trades",
        showlegend=False,
        yaxis=dict(
            title='% Profitable',
            tickformat=".0%"  # This now correctly formats the y-axis labels
        ),
        xaxis_title='Market Series'
    )
    fig.update(layout_showlegend=False)
    fig.update_yaxes(fixedrange=True)
    fig.update_xaxes(fixedrange=True)
                        
                        
    return fig

    
def bar_chart_total_return(data):
    
    with open(data, 'r') as f:
    # 'r' means open the file in read mode
        loaded_data = json.load(f)
    
    returns = loaded_data
    
    for keys, values in zip(returns.keys(), returns.values()): 
      
        processed_returns = {
        key: round(sum(values), 2) for key, values in returns.items()
    }
    
    # Explicitly convert the dictionary keys and values to lists
    market_series = list(processed_returns.keys())
    total_returns = list(processed_returns.values())
    colors = ['indianred' if val < 0 else 'rgb(55, 83, 109)' for val in total_returns]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=market_series,
        y=total_returns,
        name='Total Return',
        marker_color=colors,

    ))

    # Update properties of the BARS
    fig.update_traces(
        # Corrected the text template format
        texttemplate='$%{y:.2f}', 
        textposition='outside',
    )

    # Update properties of the LAYOUT
    fig.update_layout(
        title_text="Total Return by Market",
        xaxis_title='Market Series',
        yaxis_title='Total Return ($)',
        showlegend=False, # This is the only line needed to hide the legend
    )
    
    fig.update_yaxes(fixedrange=True)
    fig.update_xaxes(fixedrange=True)
                                
    return fig
    
    



        
            
        
        
                

 
        
        
            
    