import streamlit as st
import requests
import time
from dotenv import load_dotenv
import os
from tools import visual,utility


load_dotenv()

# Must be first Streamlit call
st.set_page_config(layout='wide', page_title='Crypto Stat Arb Trading App')

host = os.getenv("FASTAPI_HOST", "localhost")
# st.title("Copula Live Data")

try:
    data = requests.get(f"http://{host}:8000/live-data", timeout=60).json()

    if data.get('status') == 'initializing' or not data.get('coin1'):
        st.warning("Bootstrapping — fetching data and fitting model...")

    else:
        rho               = data.get('rho')
        dof               = data.get('dof')
        alpha             = data.get('alpha', 0.20)
        u1_formation      = data.get('u1') or []
        u2_formation      = data.get('u2') or []
        alt1_prices_fit   = data.get('alt1_prices_fit') or []
        alt2_prices_fit   = data.get('alt2_prices_fit') or []
        recent_alt1_price = data.get('recent_alt1_price') or []
        recent_alt2_price = data.get('recent_alt2_price') or []
        recent_dt_index   = data.get('recent_dt_index') or []
        signal_history    = data.get('signal_history') or []
        api_dt_index      = data.get('api_dt_index') or []
        crypto_historical = data.get('crypto_historical') or []
        crypto_open_positions = data.get('crypto_open_positions') or []

        if not signal_history:
            h1_2_latest    = None
            h2_1_latest    = None
            h1_2_all_prior = []
            h2_1_all_prior = []
        else:
            latest_entry   = signal_history[-1]
            h1_2_latest    = latest_entry.get('h1_2')
            h2_1_latest    = latest_entry.get('h2_1')
            history_slice  = signal_history[:-1]
            h1_2_all_prior = [d.get('h1_2') for d in history_slice]
            h2_1_all_prior = [d.get('h2_1') for d in history_slice]
            
            
        # col1, col2, col3 = st.columns(3)
        # with col1:         
        #     st.subheader(f"Pair: {data.get('coin1')} / {data.get('coin2')}")
        # with col2:
        #     with st.container():
        #         st.subheader('Current Open Position')
        #     with st.container():
        #         open_position = None#utility.crypto_open_positions()[0]
        #         open_position = open_position if open_position else "- - | - -"
        #         st.subheader(open_position)
        # with col3:
        #     with st.container():
        #         st.subheader('Unrealized Loss/Gain')
        #     with st.container():
        #         unrealizedpnl = None #utility.crypto_open_positions()[1]
        #         unrealizedpnl = unrealizedpnl if unrealizedpnl else "- - | - -"
        #         st.subheader(unrealizedpnl)
            
        # col1, col2, col3, col4 = st.columns(4)
        # col1.metric("Rho",       round(rho, 4) if rho else "N/A")
        # col2.metric("DoF",       round(dof, 2) if dof else "N/A")
        # col3.metric("h1_2 (Live)", round(h1_2_latest, 4) if h1_2_latest else "N/A")
        # col4.metric("h2_1 (Live)", round(h2_1_latest, 4) if h2_1_latest else "N/A")

        # Copula plot
        if len(u1_formation) < 2:
            st.warning("Waiting for formation data...")
        elif h1_2_latest is None:
            st.warning("Collecting live signals...")
        else:
            with st.container():
                st.subheader('Statiscal Arbitrage Pair Trading with Copulas')
            with st.container():
                st.markdown(
                    """
                    <ul style='font-size: 17px;'>
                    <li><b>Real-time Copula Signal Monitoring</b> — The dashboard visualizes a Student-t copula fitted to BTC-referenced spread pairs, plotting each asset's uniform marginal score in copula space with confidence bands. When the conditional probabilities breach the entry thresholds, a trading signal fires and the live point on the scatter plot moves outside the band.</li>
                    <li><b>Automated Pairs Trading Execution</b> — A Binance Futures websocket engine monitors closed 1-minute candles across 15 cryptocurrencies, selects the two altcoins most correlated with BTC via Kendall's tau, and automatically places long/short futures orders when the copula detects a statistical mispricing between the pair.</li>
                    <li><b>Formation & Live Price Tracking</b> — The dashboard combines 21 days of formation period price data with live candle closes to display a cumulative return chart, allowing the user to visually track how the selected pair has moved relative to each other since the model was last fitted.</li>
                    <li><b>Live Position & PnL Monitoring</b> — Current open futures positions and unrealized profit/loss are pulled directly from the Binance Futures API and displayed alongside the copula chart, giving the trader a complete picture of model signals, price action, and account exposure in a single view.</li>
                    <li>Tadi, M., & Witzany, J. (2025). Copula-based trading of cointegrated cryptocurrency pairs. Journal of Risk and Financial Management.</li>
                    </ul>
                    """,
                    unsafe_allow_html=True
                    
                )
            with st.container():
                col1, col2 = st.columns(2,border=True)
                
                # Left column — copula plot
                with col1:
                    fig = visual.copula_plot(
                        alpha=.05,
                        u1=u1_formation,
                        u2=u2_formation,
                        h1_2=h1_2_latest,
                        h2_1=h2_1_latest,
                        h1_2_prior=h1_2_all_prior,
                        h2_1_prior=h2_1_all_prior,
                        nu=dof,
                        rho=rho,
                    )
                    st.plotly_chart(fig, use_container_width=True,  config={'displayModeBar': False})

               # Right column — position info on top, price chart below
                with col2:
                    # Position info first
                    pos_col1, pos_col2 = st.columns(2, border=True)
                    with pos_col1:
                        st.subheader("Open Position")
                        open_position = crypto_open_positions[0]
                        st.subheader(open_position if open_position else "- - | - -")
                    with pos_col2:
                        st.subheader("Unrealized PnL")
                        unrealizedpnl = crypto_open_positions[1]
                        st.subheader(unrealizedpnl if unrealizedpnl else "- - | - -")

                    # Price chart underneath
                    if not recent_alt1_price:
                        st.warning("Collecting live price data...")
                    else:
                        fig = visual.coin_chart(
                            alt1_prices_fit=alt1_prices_fit,
                            alt2_prices_fit=alt2_prices_fit,
                            recent_alt1_price=recent_alt1_price,
                            recent_alt2_price=recent_alt2_price,
                            coin1_name=data.get('coin1'),
                            coin2_name=data.get('coin2'),
                            recent_dt_index=recent_dt_index,
                            api_dt_index=api_dt_index
                        )
                        st.plotly_chart(fig, use_container_width=True,  config={'displayModeBar': False})
                        # Historical trades below
            with st.container():
                utility.crypto_historical(data_dict=crypto_historical)

except Exception as e:
    st.error(f"Error communicating with Backend: {e}")

time.sleep(60)
st.rerun()