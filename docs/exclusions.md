# Exclusions

Perhaps you want to find items in your history which you have **not** bookmarked yet, so you can find some valuable but unsaved links quicker.

This doc covers how to get your bookmarks converted to a CSV of URLs and use that as an exclusion rule when creating the history report CSV.


## 1. Create CSV

Use the [flatten_urls.py](/tools/flatten_urls.py) tool to take a text file, extract just the URLs and then write out a new CSV with a single column of URLs. See more details in the script's docstring.

1. Follow this guide to print display names for all of your Chrome and Chromium users - [Identify Chrome Profiles](https://github.com/MichaelCurrin/url-manager/blob/master/docs/identify_chrome_profiles.md). For example, _My User_ could be stored in Chrome's configs with _Profile 3_.
2. Identify the browser user's config directory and then look for the `Bookmarks` JSON file within it. Replace `<PROFILE_NAME>` with one of `Default`, `Profile\ 1` or `Profile\ 2` etc. as required.
    ```bash
    $ # Linux
    $ view ~/.config/google-chrome/<PROFILE_NAME>/Bookmarks
    $ # macOS
    $ view ~/Application\ Support/Google/Chrome/<PROFILE_NAME>/Bookmarks
    ```
3. Using the `Bookmarks` path above, use the [flatten URLs script](/historyreport/flatten_urls.py) to parse the `Bookmarks` JSON file and write out the results to a CSV. The default configured output directory is to this project's [var](/historyreport/var) directory. The same Python script execution method from [Usage](usage.md#generate-reports) should be applied here.
    ```bash
    $ cd historyreport
    $ ./flatten_urls.py path/to/your/Bookmarks
    Writing to: /home/michael/repos/history-report/historyreport/var/exclusions.csv
    ```

See the [sample exclusions](/historyreport/var/samples/exclusions.csv) file included in this repo.


## 2. Create report

Now you can use the exclusion file created above to generate a report which excludes the URLs you've already bookmarked.

Example output is shown below using the [samples](/historyreport/var/samples) directory files.

```bash
$ cd historyreport
$ ./historyreport.py --exclude
Reading history: /home/michael/repos/history-report/historyreport/var/BrowserHistory.json
Filtering and sorting
Total events: 7
Relevant events: 6

Reading exclusions: /home/michael/repos/history-report/historyreport/var/exclusions.csv
Events after applying exclusion CSV: 5

Oldest event: 2018-08-21
Newest event: 2018-12-08

Writing page report: /home/michael/repos/history-report/historyreport/var/page_report.csv
Wrote: 4 rows (excluded duplicate URLs)

Writing page report: /home/michael/repos/history-report/historyreport/var/domain_report.csv
Wrote: 2 rows
```

You can visit some URLs in the page report and add the ones you like to your Chrome bookmarks. They will sync to the Chrome user's **Bookmarks** JSON, so if you generate the report again then the newly added bookmarks will be excluded too.
