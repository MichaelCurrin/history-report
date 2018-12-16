# History Report
> Convert a downloaded Chrome browser history JSON file to a more readable CSV file.

If you want to find a domain or page in your Chrome history or rediscover URLs you want to read or bookmark, you can easily make a dump of your Chrome browser data.

However, the result is a JSON file which is not in a convenient format. Therefore this project provides a tool to convert that file to a CSV that excludes irrelevant data, has duplicates removed and is easy to search, filter and sort in a CSV editor.


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

Install Python.

```bash
brew install python3
```


### Clone repo

```bash
git clone git@github.com:MichaelCurrin/history-report.git
cd path/to/history-report/historyreport/
cp config.template.py configlocal.py
# Set this up as needed or come back to it later.
editor configlocal.py 
```


## Usage

### Prepare input file

Download an archive file of your Chrome data includine history (and possibly any other data you want) from [Google Takeout](https://takeout.google.com/settings/takeout).

```bash
cd ~/Downloads
```

- Linux
    ```bash
    tar xvf takeout-20181208T205739Z-001.tgz
    ```
- Mac OS-X
    ```bash
    unzip takeout-20181208T205739Z-001.zip
    ```

```bash
mv Takeout/Chrome/BrowserHistory.json path/to/history-report/historyreport/var/
```

Example contents of the file:

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

# You may need to specify python3.6 or above if your system version is lower than 3.6.
python3 historyreport.py

view var/report.csv
# => year-month,timestamp,domain,path,fragment,title,full_url
# => ...,...,...
```
