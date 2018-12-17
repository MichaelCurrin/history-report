#!/usr/bin/env python3
"""
Main application file.

Convert an input Chrome browser history JSON file to a sorted CSV file with
unnecessary history events filtered out.
"""
import argparse
import csv
import datetime
import json
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
    Convert a timestamp from Chrome's epoch format to a datetime object.

    Conversion from Chrome epoch (such as for bookmark or history record)
    to unix timestamp is based on the formula here:
        http://linuxsleuthing.blogspot.co.za/2011/06/decoding-google-chrome-timestamps-in.html

    Note: The formula worked as given for timestamp values in the Chrome
    SQLite database of history data, but had to be modified to divide at the
    end, to work for the Chrome history JSON timestamp.

    :param value: Timestamp value in Chrome epoch format. As either an
        int, float or str. e.g. 1541956663477602

        From: https://stackoverflow.com/questions/539900/google-bookmark-export-date-format
            "Chrome uses a modified form of the Windows Time format
            ("Windows epoch") for its timestamps, both in the Bookmarks file
            and the history files. The Windows Time format is the number of
            100ns-es since January 1, 1601. The Chrome format is the number of
            microseconds since the same date, and thus 1/10 as large."
        See also:
            http://fileformats.archiveteam.org/wiki/Chrome_bookmarks

    :return: datetime.datetime object created from value.
    """
    unix_timestamp = (float(value) - 11644473600) / 1000000

    return datetime.datetime.fromtimestamp(unix_timestamp)


def process(event):
    """
    Convert a single browser history event to the desired format.

    :param dict event: Item from browser history.

    :return dict: Input item with original URL and title, URL components
        and parsed forms of the timestamp.
    """
    url_parts = urlsplit(event['url'])
    timestamp = from_chrome_epoch(event['time_usec'])

    return {
        'year_month': timestamp.strftime('%Y-%m'),
        'timestamp': timestamp,
        'domain': url_parts.netloc,
        'path': url_parts.path,
        'query': url_parts.query,
        'fragment': url_parts.fragment,
        'title': event['title'],
        'full_url': event['url'],
    }


def main():
    """
    Main application command-line function.
    """
    parser = argparse.ArgumentParser(
        description="History Report application. Convert browser history JSON"
                    " to a CSV report.")
    parser.add_argument(
        '-e', '--exclude',
        action='store_true',
        help="If provided, the configured exclusions file CSV be read and any"
             " URLs in the file will be excluded when writing the CSV report."
    )
    args = parser.parse_args()
    if args.exclude:
        exclusion_path = configlocal.CSV_EXCLUSION_PATH
        print(f"Reading from: {exclusion_path}\n")
        with open(exclusion_path) as f_in:
            reader = csv.DictReader(f_in)
            exclude_urls = set(row['url'] for row in reader)
    else:
        exclude_urls = None

    in_path = configlocal.JSON_HISTORY_PATH
    print(f"Reading from: {in_path}")
    with open(in_path) as f_in:
        data = json.load(f_in)

    print("\nProcessing data")
    history = data['Browser History']
    # Restrict URLs which are internal protocols (such as for chrome extensions
    # or system views) for unwanted ones such as 'ftp').
    print(f"Total events: {len(history)}")
    history = [process(event) for event in history
               if event['page_transition'] not in IGNORE_EVENTS
               and event['url'].startswith('http')]
    history = [x for x in history if x['domain']
               not in configlocal.IGNORE_DOMAINS]
    # Do a double sort to effectively sort by full_url ascending and timestamp
    # descending, so we use the recent timestamp when writing without duplicates.
    history.sort(key=lambda x: x['timestamp'], reverse=True)
    history.sort(key=lambda x: x['full_url'])
    print(f"Relevant events: {len(history)}")

    if exclude_urls:
        history = [x for x in history if x['full_url'] not in exclude_urls]
        print(f"Events after applying exclusion CSV: {len(history)}")

    timestamps = [x['timestamp'] for x in history]
    print(f"Oldest event: {min(timestamps).date()}")
    print(f"Newest event: {max(timestamps).date()}")

    out_path = configlocal.CSV_REPORT_PATH
    print(f"\nWriting to: {out_path}")
    with open(out_path, 'w') as f_out:
        header = (
            'year_month',
            'timestamp',
            'domain',
            'path',
            'query',
            'fragment',
            'title',
            'full_url',
        )
        writer = csv.DictWriter(f_out, fieldnames=header)
        writer.writeheader()

        wrote_count = 0
        # Skip rows which contain a duplicate of the previous row's URL.
        # We've sorted by URL and then timestamp
        previous_row = None
        for row in history:
            if previous_row is None or row['full_url'] != previous_row['full_url']:
                writer.writerow(row)
                wrote_count += 1
            previous_row = row
        print(f"Wrote: {wrote_count} rows (excluded duplicate URLs)")


if __name__ == '__main__':
    main()
