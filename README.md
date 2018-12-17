# History Report
> Convert a downloaded Chrome browser history JSON file to a more convenient CSV file.

If you want to find a domain or page in your Chrome history or rediscover URLs you want to read or bookmark, you can easily make a dump of your Chrome browser data. However, the result is a JSON file which is not in a convenient format. Therefore this project provides a tool to convert that file to more usable CSV format, One that excludes irrelevant data, has duplicates removed and is easy to search, filter and sort in a CSV editor.


## Privacy notice

Your browsing history is kept private when using this project. 

This project does *not* require access to the internet except during setup. Your Google account details are not needed directly for this application and no data is sent outside of it. The only output is local CSV files.
 

## Installation

### OS-level dependencies


- python>=3.6

#### Linux

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3 --upgrade
```

#### Mac OS-X

Install [Homebrew](https://brew.sh/).

Then install the newest version of Python 3.

```bash
brew install python
```


### Clone repo

```bash
git clone git@github.com:MichaelCurrin/history-report.git
```

### Configure

```bash
cd path/to/history-report/historyreport/
cp config.template.py configlocal.py
# Modify the local file to be setup as required, or come back to
# this later after you've seen how the CSV output needs tweaking.
editor configlocal.py 
```


## Usage

### Prepare input file

Login to your Google account in the browser, go to [Google Takeout](https://takeout.google.com/settings/takeout), then download an archive file of your data with at least history ticked. Select `.tgz` format for Linux or `.zip` format for Mac OS-X.

Find the file in default download directory.

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

```bash
mv Takeout/Chrome/BrowserHistory.json path/to/history-report/historyreport/var/
```

Example contents of the JSON file:

```json
{
    "Browser History": [
        {
            "page_transition": "LINK",
            "title": "Title goes here.",
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
        },
        ...
    ]
}
```

### Run


```bash
cd path/to/history-report/historyreport

# If you system default of Python is >= 3.6 then do this.
./historyreport.py
# Otherwise do this with an appropriate installed version.
python3.6 historyreport.py

view var/report.csv
# => year-month,timestamp,domain,path,fragment,title,full_url
# => ...,...,...
```

You can go back to [Configure](#configure) to choose alternative input or output paths, or to set domains to ignore. Then run the application again.
