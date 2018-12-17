# History Report
> Convert a downloaded Chrome browser history JSON file to a more convenient CSV file.

If you want to find a domain or page in your Chrome history or rediscover URLs you want to read or bookmark, you can easily make a dump of your Chrome browser data. However, the result is a JSON file which is not in a convenient format. 

Therefore this project provides a tool to convert that file to more usable CSV format, One that excludes irrelevant data, has duplicate URLs removed and is easy to search, filter and sort in a CSV editor.

```bash
$ history-report/historyreport.py
Reading from: /home/michael/repos/history-report/historyreport/var/BrowserHistory.json

Processing data
Total events: 16492
Total relevant events: 9757
Oldest event: 2017-11-23
Newest event: 2018-12-08

Writing to: /home/michael/repos/history-report/historyreport/var/report.csv
Wrote: 6157 rows (excluded duplicate URLs)
```

See example JSON input in the [Page report](docs/usage.md#page-report) section. The CSV output format is covered in the [View report](docs/usage.md#view-reports) section.


## Privacy notice

Your browsing history is kept private when using this project. 

This project does *not* require access to the internet except during setup. Your Google account details are not needed directly for this application and no data is sent outside of it. The only output is local CSV files.
