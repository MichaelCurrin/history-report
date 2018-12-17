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
cd path/to/history-report/historyreport/etc
cp config.template.py configlocal.py
```

You can either use the defaults copied from the [template](historyreport/etc/config.template.py), or customise your local config file. For example, you way wish to change the input or output filenames (limited to files in the [var](historyreport/var) directory). Or add unwanted high-volume domains to the ignore list, so that the report will be shorter.

```bash
editor configlocal.py 
```
