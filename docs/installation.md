# Installation


## Project requirements

- _Python_ 3.6 or above is necessary, without any additional Python libraries.

## Install OS-level dependencies

### macOS

Install [brew](https://brew.sh/).

Install packages with `brew`.

```bash
$ brew install python
```

### Ubuntu/Debian

Install packages with `apt` if you have it, otherwise `apt-get` can be used instead.

```bash
$ sudo apt update
$ sudo apt install python3
```


## Clone repo

```bash
$ git clone git@github.com:MichaelCurrin/history-report.git
$ cd history-report
```

## Configure

```bash
$ cd historyreport/etc
$ cp config.template.py configlocal.py
```

You can either use the defaults copied from the [template](/historyreport/etc/config.template.py), or customize your local config file. For example, you way wish to change the input or output filenames (limited to files in the [var](/historyreport/var) directory). Or add unwanted high-volume domains to the ignore list, so that the report will be shorter.

```bash
$ editor configlocal.py
```
