# History Report
> Convert a downloaded Chrome history JSON file to a more convenient CSV

If you want to find a domain or page in your Chrome history or rediscover URLs you want to read or bookmark, you can easily make a dump of your Chrome browser data. However, the result is a JSON file which is not in a convenient format. 

Therefore this project provides a tool to convert that file to more usable CSV format, One that excludes irrelevant data, has duplicate URLs removed and is easy to search, filter and sort in a CSV editor.

## Example

```bash
$ ./historyreport.py
Reading history: /home/michael/repos/history-report/historyreport/var/BrowserHistory.json
Removing ignored events and domains and sorting
Total events: 16492
Relevant events: 9253

Skipping exclusions

Oldest event: 2017-11-23
Newest event: 2018-12-08

Writing page report: /home/michael/repos/history-report/historyreport/var/page_report.csv
Wrote: 5948 page report rows (excluded duplicate URLs)

Writing page report: /home/michael/repos/history-report/historyreport/var/domain_report.csv
Wrote: 1531 domain report rows
```

See example JSON input in the [Page report](docs/usage.md#page-report) section. The CSV output format is covered in the [View report](docs/usage.md#view-reports) section.


## Documentation

Setup and run the application using the following docs in the [docs](docs) directory:

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)


## Privacy notice

Your browsing history is kept private when using this project. 

This project does *not* require access to the internet except during setup. Your Google account details are not needed directly for this application and no data is sent outside of it. The only output is local CSV files.
