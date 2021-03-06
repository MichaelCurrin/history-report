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
from collections import Counter
from urllib.parse import urlsplit

from etc import configlocal


# Filter history events to exclude any which have page transition which matches
# one of these. These are not usable to us by their nature and there is no
# need to add this as a field in the user config file.
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


def process_event(event):
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


def process_history(raw_history, ignore_domains=None):
    """
    Filter and sort given history data.

    :param raw_history: list of history events.
    :param ignore_domains: list of domains to filter out (using exact match
        on each event's domain value). Defaults to None to not remove matching
        domains.

    :return history: iterable of history events, with filtering and
        sorting applied.
    """
    # Restrict URLs which are internal protocols (such as for chrome extensions
    # or system views) for unwanted ones such as 'ftp').
    print(f"Total events: {len(raw_history)}")

    history = [process_event(event) for event in raw_history
               if event['page_transition'] not in IGNORE_EVENTS
               and event['url'].startswith('http')]

    if ignore_domains:
        history = [x for x in history if x['domain'] not in ignore_domains]

    # Do a double sort, to effectively sort by full_url ascending and timestamp
    # descending. This means that after excluding duplicates later when writing
    # out, each event will have the most recent timestamp from its duplicate
    # group.
    history.sort(key=lambda x: x['timestamp'], reverse=True)
    history.sort(key=lambda x: x['full_url'])

    return history


def write_page_report(out_path, history):
    """
    Write out page report from given path and data.

    Rows which contain duplicate URLs will be skipped. The data is expected to
    be sorted already so duplicates are removed by comparing consecutive rows.

    :param out_path: Path of CSV to write page report to.
    :param history: History data to use.

    :return: Count of rows written out.
    """
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

    with open(out_path, 'w') as f_out:
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

    return wrote_count


def write_domain_report(out_path, history):
    """
    Write out domain report from given path and data.

    Duplicate URLs occurrences still count to the page count for a domain.

    :param out_path: Path of CSV to write report to.
    :param history: History data to use. This is aggregated to domain values
        and counts.

    :return: Count of rows written out.
    """
    domain_counter = Counter(page['domain'] for page in history)
    domain_rows = [
        {'domain': k, 'page_count': v} for k, v in domain_counter.items()
    ]
    domain_rows.sort(key=lambda x: x['domain'])

    header = ('domain', 'page_count')

    with open(out_path, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=header)
        writer.writeheader()
        writer.writerows(domain_rows)

    return len(domain_rows)


def history_reports(history_in_path, page_report_path, domain_report_path,
                    exclusion_path=None):
    """
    Read history file, remove ignore and exclude value and write out reports.

    :param history_in_path: Path to history JSON file to read in from.
        This data will be processed, filtered and sorted.
    :param page_report_path: Path to page report to write out to.
    :param domain_report_path: Path to domain report to write out to.
    :param exclusion_path: Optional path to exclusions CSV file to read in from.
        If set, use URL values in the file as exclusion rule for page report
        data.

    :return: None.
    """
    print(f"Reading history: {history_in_path}")
    with open(history_in_path) as f_in:
        in_data = json.load(f_in)['Browser History']

    print("Filtering and sorting")
    history = process_history(
        in_data,
        configlocal.IGNORE_DOMAINS
    )
    print(f"Relevant events: {len(history)}")

    if exclusion_path:
        print(f"\nReading exclusions: {exclusion_path}")
        with open(exclusion_path) as f_in:
            reader = csv.DictReader(f_in)
            exclude_urls = set(row['url'] for row in reader)

        history = [x for x in history if x['full_url'] not in exclude_urls]
        print(f"Events after applying exclusion CSV: {len(history)}")
    else:
        print("\nSkipping exclusions")

    timestamps = [x['timestamp'] for x in history]
    print(f"\nOldest event: {min(timestamps).date()}")
    print(f"Newest event: {max(timestamps).date()}")

    print(f"\nWriting page report: {page_report_path}")
    page_rows = write_page_report(
        page_report_path,
        history,
    )
    print(f"Wrote: {page_rows} rows (excluded duplicate URLs)")

    print(f"\nWriting page report: {domain_report_path}")
    domain_rows = write_domain_report(
        domain_report_path,
        history,
    )
    print(f"Wrote: {domain_rows} rows")


def main():
    """
    Main application command-line function.

    Handle command-line arguments then read, process and write data.
    """
    parser = argparse.ArgumentParser(
        description="History Report application. Convert browser history JSON"
                    " to a CSV report."
    )
    parser.add_argument(
        '-e', '--exclude',
        action='store_true',
        help="If provided, read the configured exclusions CSV and exclude any"
             " URLs in the file before writing the CSV report."
    )
    args = parser.parse_args()

    history_reports(
        history_in_path=configlocal.JSON_HISTORY_PATH,
        page_report_path=configlocal.CSV_URL_REPORT_PATH,
        domain_report_path=configlocal.CSV_DOMAIN_REPORT_PATH,
        exclusion_path=configlocal.CSV_EXCLUSION_PATH if args.exclude else None,
    )


if __name__ == '__main__':
    main()
