# History Report
> Create page and domain CSV reports from your Chrome browsing history

Google Chrome lets you view and search your browsing history, although with limitations on metadata and the ability to filter or sort. Though you can export your data to an XML file from the browser or get a JSON download from your Google account, those raw data files are still inconvenient to use.

Therefore this project provides Python 3.6 tool to convert your own downloaded browsing history JSON into two easy-to-use CSV reports which you can search, filter and sort in a CSV editor.

Title             | Description
---               | ---
**Page Report**   | List of URLs in the history events, including the last visit time, domain and page title. Sorted by URL.
**Domain Report** | Summary of unique domains and counts of pages associated with each. Sorted by domain but easily sortable by page count.


## Example usage

### Command

```bash
$ ./historyreport.py
```

### Flags

Flag         | Description
---          | ---
-h           | Show help message and exit.
-e --exclude | If provided, read the configured exclusions CSV and exclude any URLs in the file before writing the CSV report.

### Samples

Sample input files:

- [BrowserHistory.json](/historyreport/var/samples/BrowserHistory.json)
- [exclusions.csv](/historyreport/var/samples/exclusions.csv)

Sample output files:

- [page_report.csv](/historyreport/var/samples/page_report.csv)
- [domain_report.csv](/historyreport/var/samples/domain_report.csv)


## Exclusions

When creating the reports, certain domains or URLs will be excluded. This is done with a config, containing app defaults and user-defined items. For example, the app will ignore _www.facebook.com_ and you might decided to exclude Such as _gmail.com_.

This project cares about browsing events, so irrelevant events are ignored and define in `IGNORE_EVENTS` in [historyreport.py](history-report/historyreport/historyreport.py). 

In that script, only _http_ and _https_ URLs are used, filtering out items like local file paths (`file:///`) and FTP URLs (`ftp://`).


## Documentation

Setup and run the application with the following in the [docs](docs) directory:

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)


## Privacy notice

Your browsing history is kept private when using this project.

This project does *not* require access to the internet except during setup. Your Google account details are not needed directly for this application and no data is sent outside of it. The only output is local CSV files.
