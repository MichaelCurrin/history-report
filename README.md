# History Report
> Convert a downloaded Chrome browser history JSON file to a more convenient CSV file.

If you want to find a domain or page in your Chrome history or rediscover URLs you want to read or bookmark, you can easily make a dump of your Chrome browser data. However, the result is a JSON file which is not in a convenient format. Therefore this project provides a tool to convert that file to more usable CSV format, One that excludes irrelevant data, has duplicates removed and is easy to search, filter and sort in a CSV editor.


## Privacy notice

Your browsing history is kept private when using this project. 

This project does *not* require access to the internet except during setup. Your Google account details are not needed directly for this application and no data is sent outside of it. The only output is local CSV files.
 

## Installation

### 1. OS-level dependencies


Python 3.6 or above is necessary, without any additional Python libraries. 


#### Linux

```bash
sudo apt update
sudo apt install python3 --upgrade
```

#### Mac OS-X

Install [Homebrew](https://brew.sh/).

Then install the newest version of Python 3.

```bash
brew install python
```


### 2. Clone repo

```bash
git clone git@github.com:MichaelCurrin/history-report.git
```

### 3. Configure

```bash
cd path/to/history-report/historyreport/
cp config.template.py configlocal.py
```

You can either use the defaults copied from the [template](historyreport/etc/config.template.py), or customise your local config file. For example, you way wish to change the input or output filenames (limited to files in the [var](historyreport/var) directory), or add domains to ignore so that the report will be shorter.

```bash
editor configlocal.py 
```


## Usage

### 1. Prepare input data

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

Example contents of the JSON file:

```json
{
    "Browser History": [
        {
            "page_transition": "LINK",
            "title": "Example title.",
            "url": "https://example.com",
            "client_id": "XXXXXXXX",
            "time_usec": 1544302609251723
        },
        {
            "page_transition": "TYPED",
            "title": "Fast Dial - New tab",
            "url": "chrome://newtab/",
            "client_id": "XXXXXXXX",
            "time_usec": 1544302601079441
        }
    ]
}
```

### 2. Run

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

### 3. View report

The path to the output file will be shown by the run command above. Open the file with a CSV editor or a file viewer.

```bash
view var/report.csv
```

Each row in the CSV is a browser history action or event from the input file as can be thought of as a visit to a URL at a specific time.

Field definitions:

- **year_month**: Date of page visit, in `YYYY-MM` format.
- **timestamp**: Date and time of page visit, in ISO format.
- **domain**: The domain is the website hostname without any protocol. This may start with `www.`.
- **path**: The page path and optional query parameters. Excludes the domain.
- **fragment**: Optional hash identifier for HTML anchor tag on the page. This is typically a section heading.
- **full_url**: The original URL from the source data. This includes the domain, path and fragment components.

Example file:

```csv
year_month,timestamp,domain,path,fragment,title,full_url
2018-12,2018-12-08 18:13:56.112307,github.com,/MichaelCurrin,,MichaelCurrin (Michael Currin),https://github.com/MichaelCurrin
...
```

You may wish to go and make changes in the [Configure](#3-configure) step and then run the application again.
