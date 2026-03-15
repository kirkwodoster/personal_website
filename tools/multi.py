# tools/multi.py
import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys
import multiprocessing
from datetime import datetime
from tools import scrape # Make sure this path is correct
import pandas as pd
import os
import sys
import logging
import time # <--- IMPORT TIME

# def start_scraper_multiprocess():
#     """
#     Starts the scraper process if it's not already running.
#     Uses a global variable to track the process.
#     """
#     if 'scraper_process' not in st.session_state:
#         st.session_state.scraper_process = None

#     if st.session_state.scraper_process is None or not st.session_state.scraper_process.is_alive():
#         ctx = multiprocessing.get_context("spawn")
#         st.session_state.scraper_process = ctx.Process(target=start_scraper_process, name="TemperatureScraper")
#         st.session_state.scraper_process.daemon = True
#         st.session_state.scraper_process.start()
#         # st.info(f"Started background scraper process (PID: {st.session_state.scraper_process.pid})")
#         time.sleep(5) # Give a moment for initial scrape

# # Configure logging for the background script
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler()]
# )
# logger = logging.getLogger(__name__)

# def start_scraper_process():

#     scheduler = BackgroundScheduler()

#     scheduler.add_job(scrape.scrape_to_csv, 'interval', minutes=1)
#     try:
#         scrape.scrape_to_csv()

#     except Exception as e:
#         logger.error(f"[{os.getpid()}] Initial scrape failed: {e}", exc_info=True)

#     scheduler.start()
#     try:
#         while True:
#             time.sleep(1) # Sleep for a short period to keep the main thread alive
#     except (KeyboardInterrupt, SystemExit):
#         logger.info(f"[{os.getpid()}] Scraper process received shutdown signal. Shutting down scheduler.")
#         scheduler.shutdown()
#     except Exception as e:
#         logger.critical(f"[{os.getpid()}] Scheduler process encountered a critical error: {e}", exc_info=True)

# if __name__ == '__main__':
#     start_scraper_process()


# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)

# def scraper_worker():
#     """Independent worker function that runs in its own process"""
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(
#         scrape.scrape_to_csv,
#         'interval',
#         minutes=1,
#         max_instances=1
#     )
    
#     try:
#         # Initial run
#         scrape.scrape_to_csv()
#         scheduler.start()
        
#         # Keep process alive
#         while True:
#             time.sleep(5)
#     except Exception as e:
#         logger.error(f"Scraper failed: {e}")
#     finally:
#         scheduler.shutdown()

# def start_scraper():
#     """Safe process starter that handles Streamlit's reload behavior"""
#     if not hasattr(st.session_state, 'scraper_process'):
#         ctx = multiprocessing.get_context("spawn")
#         st.session_state.scraper_process = ctx.Process(
#             target=scraper_worker,
#             daemon=True
#         )
#         st.session_state.scraper_process.start()
#         time.sleep(2)  # Allow initial scrape to complete