"""
Config module.
"""
import os


APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAR_DIR = os.path.join(APP_DIR, 'var')

JSON_HISTORY_PATH = os.path.join(VAR_DIR, 'BrowserHistory.json')
CSV_REPORT_PATH = os.path.join(VAR_DIR, 'report.csv')
CSV_EXCLUSION_PATH = os.path.join(VAR_DIR, 'exclusions.csv')


IGNORE_DOMAINS = frozenset((
    'm.facebook.com',
    'facebook.com',
    'www.google.com',
    'www.youtube.com',
    'www.instagram',
))
