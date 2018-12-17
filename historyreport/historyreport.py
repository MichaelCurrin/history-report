#!/usr/bin/env python3
"""
Main application file.
"""
import csv
import json
import datetime
from urllib.parse import urlsplit

from etc import configlocal


# Events which are not that useful and so can be ignored.
IGNORE_EVENTS = (
    'GENERATED',     # Google searches
    'AUTO_TOPLEVEL', # New tab
    'FORM_SUBMIT'    # Submit to a form which you probably already visited
)


def from_chrome_epoch(value):
    """
    Convert from Chrome epoch to datetime object.

    The way to get unix timestamp value comes from researched formula. It
    worked for the timestamp values in the Chrome SQLite database of history
    data, but had to be modified to be a million times smaller to convert from
    the microsecond value in a downloaded history JSON file.
    """
    unix_timestamp = (float(value) - 11644473600) / 1000000

    return datetime.datetime.fromtimestamp(unix_timestamp)


def process(event):
    """
    Convert a single browser history event to the desired format.

    :param dict event: Item from browser history.

    :return dict: Input item with original URL and title, the URL as components
        and parsed forms of the timestamp.
    """
    url_parts = urlsplit(event['url'])
    timestamp = from_chrome_epoch(event['time_usec'])

    return {
        'year_month': timestamp.strftime('%Y-%m'),
        'timestamp': timestamp,
        'domain': url_parts.netloc,
        'path': url_parts.path,
        'fragment': url_parts.fragment,
        'title': event['title'],
        'full_url': event['url'],
    }


def main():
    """
    Main application command-line function.
    """
    in_path = configlocal.JSON_HISTORY_PATH
    print(f"Reading from: {in_path}")
    with open(in_path) as f_in:
        text = f_in.read()

    print("Processing data")
    history = json.loads(text)['Browser History']
    # Restrict URLs which are internal protocols (such as for chrome extensions
    # or system views) for unwanted ones such as 'ftp').
    history = [process(event) for event in history
               if event['page_transition'] not in IGNORE_EVENTS
               and event['url'].startswith('http')]
    history = [x for x in history if x['domain']
               not in configlocal.IGNORE_DOMAINS]

    history.sort(key=lambda x: x['full_url'])

    out_path = configlocal.CSV_REPORT_PATH
    print(f"Writing to: {out_path}")
    with open(out_path, 'w') as f_out:
        header = (
            'year_month',
            'timestamp',
            'domain',
            'path',
            'fragment',
            'title',
            'full_url',
        )
        writer = csv.DictWriter(f_out, fieldnames=header)
        writer.writeheader()

        # Skip rows which contain a duplicate of the previous row's URL.
        previous_row = None
        for row in history:
            if previous_row is None or row['full_url'] != previous_row['full_url']:
                writer.writerow(row)
            previous_row = row


if __name__ == '__main__':
    main()
