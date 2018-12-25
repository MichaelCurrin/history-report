# Usage

This doc covers usage instructions to get the required history JSON file and run the main application to generate two CSV reports.


## Prepare input data

The [historyreport.py](/historyreport/historyreport.py) script was written based on the format of a downloaded JSON file of Chrome history. See the short [sample browser history JSON](/historyreport/var/samples/BrowserHistory.json) file which is provided in the repo.

Follow these steps to download a JSON file with your own data then move it to the project:

1. Login to your Google account in a browser.
2. Go to [Google Takeout](https://takeout.google.com/settings/takeout), then download an archive file of your data with at least the history section ticked. Select `.tgz` format for Linux or `.zip` format for Mac OS-X.
3. Find and unzip the downloaded archive.
    ```bash
    $ cd ~/Downloads
    $ # Either
    $ tar xvf takeout-2019XXXXXXXXXXXX-001.tgz
    $ # Or
    $ unzip takeout-2019XXXXXXXXXXXX-001.zip
    ```
4. Copy the file to the project.
    ```bash
    $ mv Takeout/Chrome/BrowserHistory.json <PATH_TO_REPO>/historyreport/var/
    ```

### Notes

- Downloading and using the file will only work if have something in your Chrome browsing history, have signed into Google with Chrome and have synced your browsing activity to your Google account.
- Although there is _SQLite_ database file for each Chrome user which will history activity, that only contains _locally_ created data and not data from the same profile across other devices, so is not used in this project.


## Generate reports

Once you have a _BrowserHistory.json_ file as covered by the section above, use the following steps to create a CSV file from it as an easy-to-explore report on your browser history.

```bash
$ cd <PATH_TO_REPO>/historyreport/
```

Use your system's Python without a virtual environment. Check what your system's default is.

```bash
$ python -V
python3.5.3
```

If your system's _default_ is `3.6` or higher, use:

```bash
$ ./historyreport.py
```

Otherwise specify the version manually:

```bash
$ python3.6 historyreport.py
```

If you want to provide a list of URLs to exclude when running the above command, then see the [exclusions](exclusions.md) docs on using the `--exclude` flag.


## View reports

You can open the file with a CSV editor or a file viewer. Use the paths printed in the output above or use the instructions below.


```bash
$ cd <PATH_TO_REPO>/historyreport/var
```

### Page report

Each row in the CSV is the most action performed for a URL, with a specific time at a specific time.

```bash
$ view page_report.csv
```

See also the [sample page report](/historyreport/var/samples/page_report.csv) provided in the repo.

Field definitions:

- **year_month**: Date of the _most recent_ visit to a page, in `YYYY-MM` format.
- **timestamp**: Date and time of the _most recent_ visit to page, in ISO format.
- **domain**: The domain is the website hostname without any protocol. This may start with `www.`.
- **path**: The page path and optional query parameters. Excludes the domain.
- **query**: Query parameters string.  For some websites, the query defines the search results or page you are looking at, so is functional. But sometimes it is just UTM tracking data.
- **fragment**: Optional hash identifier for HTML anchor tag on the page. This is typically a section heading.
- **title**: Title of the page.
- **full_url**: The original URL from the source data. It should have the following pattern: `scheme://netloc/path;params?query#fragment` (based on the `urllib` library's `ParseResult.geturl()` result). The params component is not included as its own column.


Chrome history only seems to keep the most recent visit to a page for an event type. If a URL appears across different events (e.g. `RELOAD` and `LINK`) then the most recent entry in the duplicate set is used and the others are dropped for this report.

You may wish to go and make changes in the [Configure](installation.md#configure) step and then run the application again.


### Domain report


This is a summary report using the same source data. This domain report should be shorter and can give you an overview of domains and possibly ideas to add to the ignore list before running the report generation again.


```bash
$ view domain_report.csv
```

See also the [sample domain report](/historyreport/var/samples/domain_report.csv) provided in the repo.

Field definitions:

- **domain**: URL domain, excluding the http or https protocol.
- **pages**: Count of URLs associated with this page. Duplicates are included in the count.
