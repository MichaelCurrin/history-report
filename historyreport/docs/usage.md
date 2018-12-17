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
    ```
    - Linux
        ```bash
        tar xvf takeout-2019XXXXXXXXXXXX-001.tgz
        ```
    - Mac OS-X
        ```bash
        unzip takeout-2019XXXXXXXXXXXX-001.zip
        ```
4. Copy the file to the project.
    ```bash
    mv Takeout/Chrome/BrowserHistory.json path/to/history-report/historyreport/var/
    ```


## Generate report

Once you have a _BrowserHistory.json_ file as covered by the section above, use the following steps to create a CSV file from it as an easy-to-explore report on your browser history.

```bash
cd path/to/history-report/historyreport
```

```bash
# If your system default of Python is >= 3.6 then do this.
./historyreport.py
# Otherwise do this, using an appropriate installed version.
python3.6 historyreport.py
```

If you want to provide a list of URLs to exclude when running the above command, then see the [exclusions](exclusions.md) docs.


## View report

The path to the output file will be shown by the run command above. Open the file with a CSV editor or a file viewer.

```bash
view var/report.csv
```

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

```csv
year_month,timestamp,domain,path,query,fragment,title,full_url
2018-12,2018-12-08 18:13:56.112307,github.com,/MichaelCurrin,,,MichaelCurrin (Michael Currin),https://github.com/MichaelCurrin
...
```

You may wish to go and make changes in the [Configure](installation.md#configure) step and then run the application again.
