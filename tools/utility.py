from tools import inputs
from tools.clients import client
from datetime import datetime
import pytz
import pandas as pd
import streamlit as st
import os
import plotly.graph_objects as go
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

### Kalshi Weather Algo ###
def yes_title(position: str):
    ticker = position.get('ticker')
    event_strip = ticker.split('-')[0:2]
    event_ticker = event_strip[0] + '-' + event_strip[1]
    event = client.get_event(event_ticker=event_ticker)
    markets = event.get('markets')
    for i in markets:
        ticker_find = i.get('ticker')
        if ticker == ticker_find:
            yes_title = i.get('yes_sub_title')
            
            return yes_title

    
    try:
        ticker = position.get('ticker')
        series = position.get('ticker').split('-')[0]
        all_cities = inputs.all_markets().keys()
        all_makets_dict = inputs.all_markets()
        
        for i in all_cities:
            if all_makets_dict.get(i).get('SERIES') == series:
                city = i
                
                status = position.get('status')
                maker = position.get('maker_fill_cost')
                taker = position.get('taker_fill_cost')
                limit = maker if taker == 0 else taker
                
                try:
                    current_ask = client.get_market_order_book(ticker=ticker).get('orderbook').get('yes')[-1][0]
                except:
                    current_ask = 0
                    
                time_str = position.get('created_time')
                time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                timezone = all_makets_dict[city].get('TIMEZONE')
                local_time = time_obj.replace(tzinfo=pytz.utc).astimezone(timezone)
                local_time_str = local_time.strftime('%Y-%m-%d %H:%M')
        
                return {'City': city, 'Series': series, 'Status': status, 'Fill Price': limit, 'Market Price': current_ask, 'Date': local_time_str}
    except Exception as e:
        print(f'Portfolio Tracker: {e}')

def portfolio_tracker(position: dict):
    
    try:
        ticker = position.get('ticker')
        series = position.get('ticker').split('-')[0]
        all_cities = inputs.all_markets().keys()
        all_makets_dict = inputs.all_markets()
        
        for i in all_cities:
            if all_makets_dict.get(i).get('SERIES') == series:
                city = i
                
                status = position.get('status')
                maker = position.get('maker_fill_cost')
                taker = position.get('taker_fill_cost')
                limit = maker if taker == 0 else taker
                
                try:
                    current_ask = client.get_market_order_book(ticker=ticker).get('orderbook').get('yes')[-1][0]
                except:
                    current_ask = 0
                    
                time_str = position.get('created_time')
                time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                timezone = all_makets_dict[city].get('TIMEZONE')
                local_time = time_obj.replace(tzinfo=pytz.utc).astimezone(timezone)
                local_time_str = local_time.strftime('%Y-%m-%d %H:%M')
        
                return {'City': city, 'Series': series, 'Status': status, 'Fill Price': limit, 'Market Price': current_ask, 'Date': local_time_str}
    except Exception as e:
        print(f'Portfolio Tracker: {e}')

        
def date_check(position: dict):

    timezone = pytz.timezone("US/Central")
    time_str = position.get('created_time')
    time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    local_time = time_obj.replace(tzinfo=pytz.utc).astimezone(timezone)
    
    if local_time.day == datetime.now(pytz.timezone("US/Central")).day:
        
        return True

    
   
def position_data():
    
    positions = client.get_positions().get('orders')[0:6]
    try:
        position_data = {
            'City': [],
            'Series': [],
            'Temp Range': [],
            'Status': [],
            'Fill Price': [],
            'Market Price': [],
            'Date': [],
        }
        for i in positions:
            status = i.get('status')
            status = status == 'resting' or status == 'executed'
            data_today = date_check(position=i)
 
            if data_today:
                yes_sub_title = yes_title(i)
                position_data['Temp Range'].append(yes_sub_title)
                tabs_data = portfolio_tracker(i)
                               
                for key, value in tabs_data.items():
                    position_data[key].append(value)
                   
            else:
                continue
     
        return position_data
    except Exception as e:
        print(f'position_data: {e}')

# @st.cache_data(ttl=360)
# @st.fragment(run_every="10s")
def position_data_chart():
    try:
        
        position_df = pd.DataFrame(position_data())
        header_style = {
                    'selector': 'th',
                    'props': [
                    ('color', 'white !important'),
              
            ]
        }
        all_cities= [i for i in inputs.all_markets().keys()]
        all_series = [i for i in inputs.series_city.keys()]
        position_dict = {
            'City': all_cities,
            'Series': all_series,
            'Temp Range': 6 * [""],
            'Status': 6 * [""],
            'Fill Price': 6 * [""],
            'Market Price': 6 * [""],
            'Date': 6 * [""],
            }
        # print(all_cities)
        if position_df.empty:
            position_df = pd.DataFrame(position_dict)
            # print('is empty')
            
        else:
            # print(position_df)
            length = len(position_df)
            total_rows = position_df.shape[0]
            counter = 0 
            max_rows = 6 -  total_rows
            col_minus_two = len(position_df.columns) - 2
            for i,j in zip(all_cities, all_series):
                if i not in position_df['City'].values:
                    # print([i]+[j]+col_minus_two * [""] )
                    position_df.loc[length+counter] = [i]+[j]+ col_minus_two * [""]
                    counter += 1
                    if counter == max_rows:
                        break
        position_df = position_df.set_index('City')            
        position_df = position_df.style.set_table_styles([header_style])
        df2 = st.table(position_df)
        return df2
    except Exception as e:
        print(e)
    # st.dataframe()
    
### Kalshi Weather Algo ###

def to_data_file():
    script_dir = os.path.dirname(os.path.abspath(__file__)) # .../kw_fe/tools
    project_root_dir = os.path.abspath(os.path.join(script_dir, os.pardir)) # .../kw_fe
    data_dir_path = os.path.join(project_root_dir, 'data') # .../kw_fe/data
    os.makedirs(data_dir_path, exist_ok=True)
    file_path_to_save = os.path.join(data_dir_path, "cached_temp_data.csv")
    
    return file_path_to_save

### Portfolio History ###
# @st.fragment(run_every="3600s")
def portfolio_history():
    
    table_dict = {
        'City':[],
        'Market': [],
        'Date': [],
        'Fill Price': [],
        'Profit/Loss': []
    }
    total = []
    history = client.get_portfolio_settlements().get('settlements')
    for i in history:
         if i.get('yes_count') == 1:
        
            market = i.get('ticker').split('-')[0]
            
            city = inputs.series_city.get(market)

            datetime_str = i.get('settled_time')
            date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()
            
            profit_loss = (i.get('revenue') - i.get('yes_total_cost'))/100
            total.append(profit_loss)
            profit_loss_sign = f"-${abs(profit_loss)}" if profit_loss < 0 else f"+${profit_loss}"
            
            fill_price = i.get('yes_total_cost')
            fill_price_formatted = str(round(fill_price,1))
            
            table_dict['City'].append(city)
            table_dict['Market'].append(market)
            table_dict['Date'].append(date)
            table_dict['Fill Price'].append(fill_price_formatted)
            table_dict['Profit/Loss'].append(profit_loss_sign)
            
            def color_profit_loss(val):
                """Color negative values red, positive green"""
                return 'color: red' if val.startswith('-') else 'color: green'
            
    # print('Total', max(total))
    df = pd.DataFrame(table_dict)
    df['City'] = df['City'].apply(lambda x: x.upper())
    
    df = df.set_index('City')
    # print(df)
    # styled_df = (df.style
    #         #  .map(color_profit_loss, subset=['Profit/Loss'])
    #         #  .format({'Fill Price': '${:,.2f}'})
    #         #  .set_table_styles([
    #         #     {'selector': 'th.col(4)', 'props': 'text-align: right;'}
    #         #  ])

    header_style = {
                    'selector': 'th',
                    'props': [
                    ('color', 'white'),          
                ]
            }
    df = df.style.set_table_styles([header_style])
    # df = df.set_index('City')
    return st.table(df)
    
    
def historical_balances():

    history = client.get_portfolio_settlements().get('settlements')
    date_list = [i.get('settled_time') for i in history if i.get('yes_count_fp') == '1.00']
    start = min(date_list).split('T')[0]
    end = datetime.now().date().strftime('%Y-%m-%d')
    date_range = pd.date_range(start, end)
    date_balance_dict = {datetime.strftime(i, '%Y-%m-%d'): [] for i in date_range}
    
    fees_dict = client.get_positions()['orders']

    balance = client.get_balance()['balance']/100
    for i in history:
        if i.get('yes_count') == 1:
            profit_loss = (i.get('revenue') - i.get('yes_total_cost'))/100
            settled_time = i.get('settled_time')
            settled_date = settled_time.split('T')[0]
            date_balance_dict[settled_date].append(profit_loss)
 
    for j in fees_dict:
        fees_datetime = j.get('last_update_time')
        fees_date = fees_datetime.split('T')[0]
        fees = j.get('taker_fees_dollars')
        fees_cents = (float(fees)) * -1
        
        try:
            date_balance_dict[fees_date].append(fees_cents)
        except:
            pass
    for k in date_balance_dict:
        try:
            date_balance_dict[k] = sum(date_balance_dict[k])
            date_balance_dict = {key: date_balance_dict[key] for key in sorted(date_balance_dict.keys(), reverse=True)}
            for keys, values in date_balance_dict.items():
                balance -= values
                date_balance_dict[keys] = round(balance,2)
                
        except:
            pass
    return date_balance_dict

##################################### Crypto Historic Trades ##########################

#######################################################################################


def crypto_historical(data_dict):
    
    header_style = {
                    'selector': 'th',
                    'props': [
                    ('color', 'white !important'),
              
            ]
        }
    
    position_df = pd.DataFrame(data_dict)#.set_index('time', inplace=True)
    position_df = position_df.set_index('Time')
    # print(position_df)
    position_df = position_df.style.set_table_styles([header_style])
    st_df = st.table(position_df)
    
    return st_df
        
