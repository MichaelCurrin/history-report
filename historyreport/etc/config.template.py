"""
Config module.
"""
import os


APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAR_DIR = os.path.join(APP_DIR, 'var')

CSV_EXCLUSION_PATH = os.path.join(VAR_DIR, 'exclusions.csv')
JSON_HISTORY_PATH = os.path.join(VAR_DIR, 'BrowserHistory.json')
CSV_URL_REPORT_PATH = os.path.join(VAR_DIR, 'page_report.csv')
CSV_DOMAIN_REPORT_PATH = os.path.join(VAR_DIR, 'domain_report.csv')


IGNORE_DOMAINS = frozenset((
    'm.facebook.com',
    'www.facebook.com',
    'www.google.com',
    'm.youtube.com',
    'www.youtube.com',
    'www.instagram',
))
