# Exclusions


Perhaps you want to find items in your history which you have **not** bookmarked yet, so you can find some valuable but unsaved links quicker. 

This doc covers how to get your bookmarks converted to a CSV of URLs and use that as an exclusion rule when creating the history report CSV.


## 1. Create CSV

Use the [flatten_urls.py](/tools/flatten_urls.py) tool to take a text file, extract just the URLs and then write out a new CSV with a single column of URLs. See more details in the script's docstring.

1. Use the [/identify_chrome_profiles.sh](https://github.com/MichaelCurrin/url-manager/blob/master/tools/identify_chrome_profiles.sh) tool in the [MichaelCurrin/url-manager](https://github.com/MichaelCurrin/url-manager) repo to identify which directory is for your Chrome user. Such as `Profile 3`.
2. Find the Chrome bookmarks file for the Chrome user you are interested in. For example:
    ```bash
    view ~/.config/google-chrome/Profile\ 3/Bookmarks
    ```
3. Use the flatten URLs tool to parse that bookmarks file and write out the results to a CSV in this project's [var](/historyreport/var) directory.
    ```bash
    $ cd historyreport
    $ ./flatten_urls.py < path/to/Bookmarks.json
    Writing to: var/exclusions.csv
    ```

Example output file:

```csv
url
http://abc.com
https://def.com
```

## 2. Create report

Now you can generate a report without URLs you've already bookmarked, by using the path to the exclusion file you created above.

```bash
$ cd historyreport
$ ./historyreport.py --exclude
Reading from: var/exclusions.csv

Reading from: /home/michael/repos/history-report/historyreport/var/BrowserHistory.json

Processing data
Total events: 16492
Relevant events: 9757
Events after applying exclusion CSV: 5443
Oldest event: 2017-11-23
Newest event: 2018-12-08

Writing to: /home/michael/repos/history-report/historyreport/var/report.csv
Wrote: 3838 rows (excluded duplicate URLs)
```

You can visit some URLs in the history report and add the ones you like to your Chrome bookmarks. They will sync to the Chrome config Bookmarks JSON, so if you generate the report again then the newly added bookmarks now be excluded too.
