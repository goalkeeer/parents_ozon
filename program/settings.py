import os
from dotenv import load_dotenv


load_dotenv()

LOG_PATH = os.environ.get('LOG_PATH', 'logs')
RESULT_PATH = os.environ.get('RESULT_PATH', 'results')

# trade lock
TRADE_LOCK_USERNAME = os.environ.get('TRADE_LOCK_USERNAME')
TRADE_LOCK_PASSWORD = os.environ.get('TRADE_LOCK_PASSWORD')

# warning value
COUNT_DIFFERENCE = int(os.environ.get('COUNT_DIFFERENCE', 5))
AMOUNT_DIFFERENCE = float(os.environ.get('AMOUNT_DIFFERENCE', 0.2))
