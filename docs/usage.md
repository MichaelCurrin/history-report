# Usage

## Prepare input data

Example contents of the JSON file:

```json
{
    "Browser History": [
        {
            "favicon_url": "https://cdn.example.com/favicon.ico",
            "page_transition": "LINK",
            "title": "Example title.",
            "url": "https://example.com",
            "client_id": "XXXXXXXXXXXXXXXXXXXXX",
            "time_usec": 1544302609251723
        },
        {
            "favicon_url": "https://assets-cdn.github.com/favicon.ico",
            "page_transition": "LINK",
            "title": "MichaelCurrin (Michael Currin)",
            "url": "https://github.com/MichaelCurrin",
            "client_id": "XXXXXXXXXXXXXXXXXXXXX",
            "time_usec": 1542445932073440
        },
        {
            "page_transition": "TYPED",
            "title": "Fast Dial - New tab",
            "url": "chrome://newtab/",
            "client_id": "XXXXXXXXXXXXXXXXXXXXX",
            "time_usec": 1544302601079441
        }
    ]
}
```

Follow these steps to download a JSON file with your own data and move it to the project:

1. Login to your Google account in a browser.
2. Go to [Google Takeout](https://takeout.google.com/settings/takeout), then download an archive file of your data with at least the history section ticked. Select `.tgz` format for Linux or `.zip` format for Mac OS-X.
3. Find and unzip the downloaded archive.
    ```bash
    cd ~/Downloads
    # Either
    tar xvf takeout-2019XXXXXXXXXXXX-001.tgz
    # Or
    unzip takeout-2019XXXXXXXXXXXX-001.zip
    ```
4. Copy the file to the project.
    ```bash
    mv Takeout/Chrome/BrowserHistory.json path/to/history-report/historyreport/var/
    ```


## Generate reports

Once you have a _BrowserHistory.json_ file as covered by the section above, use the following steps to create a CSV file from it as an easy-to-explore report on your browser history.

```bash
cd <PATH_TO_REPO>/historyreport
```

Use your system's Python without a virtual environment. Check what your system's default is.

```bash
$ python -V
python3.5.3
```

If your system's _default_ is `3.6` or higher, use:

```bash
./historyreport.py
```

Otherwise specify the version manually:

```bash
$ python3.6 historyreport.py
```

If you want to provide a list of URLs to exclude when running the above command, then see the [exclusions](exclusions.md) docs on using the `--exclude` flag.


## View reports

The path sto the output file will be shown by the run command above. Open the file with a CSV editor or a file viewer.


```bash
cd <PATH_TO_REPO>/historyreport
```

### Page report

Each row in the CSV is a browser history action or event from the input file as can be thought of as a visit to a URL at a specific time.

Field definitions:

- **year_month**: Date of the _most recent_ visit to a page, in `YYYY-MM` format.
- **timestamp**: Date and time of the _most recent_ visit to page, in ISO format.
- **domain**: The domain is the website hostname without any protocol. This may start with `www.`.
- **path**: The page path and optional query parameters. Excludes the domain.
- **query**: Query parameters string.  For some websites, the query defines the search results or page you are looking at, so is functional. But sometimes it is just UTM tracking data.
- **fragment**: Optional hash identifier for HTML anchor tag on the page. This is typically a section heading.
- **full_url**: The original URL from the source data. It should have the following pattern: `scheme://netloc/path;params?query#fragment` (based on the `urllib` library's `ParseResult.geturl()` result). The params component is not handled in this project outside of this field. 

Example file:

```bash
view var/page_report.csv
```

```csv
year_month,timestamp,domain,path,query,fragment,title,full_url
2018-12,2018-12-08 18:13:56.112307,github.com,/MichaelCurrin,,,MichaelCurrin (Michael Currin),https://github.com/MichaelCurrin
...
```

You may wish to go and make changes in the [Configure](installation.md#configure) step and then run the application again.


### Domain report

This is a summary report using the same source as above. This report should be shorter and can give you an overview of domains and possibly ideas to add to the ignore list before running the report generation again.

Field definitions:

- **domain**: URL domain, excluding the http or https protocol.
- **pages**: Count of URLs associated with this page in the [Page report](#page-report).

Example file:

```bash
view var/domain_report.csv
```

```csv
domain,pages
abc.com,5
example.com,1
```
