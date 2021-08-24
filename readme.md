# HTTP monitor

Author: Carles Garcia Cabot

This **proof-of-concept** HTTP monitor can process a web server log file,
print statistics and alert for high traffic.

## How to run
The program has been developed in a Python 3.9 environment, but I expect 
it to work with Python >= 3.7
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
python3 main.py --help
python3 main.py -i log.csv
```

## Main features
- Memory efficient: thanks to the csv library, only one row at a time is loaded, so I expect that it can support
large log files.
- Time efficient: each line is processed only once.
- To ensure code quality, the code has been checked with black, isort, mypy and pylint.
- The input file, printing interval, alert threshold and window are configurable.
  

## Potential improvements
- In a real-time scenario, we could use a real-time clock to calculate averages instead of the log file clock.
- In a real setting, we should run this as a daemon.  
- Improve test coverage: currently only the Alert is tested, ideally we should have 90% coverage or higher. 
  In addition to unit tests, we should have integration tests that run with prepared log files.
- Support multiple alarms: we could have multiple alarms for different metrics.
- The alert should support a recovery threshold that is lower than the trigger threshold to avoid potential alert flapping.

## Known issues
- The log files are not strictly sorted by time because they aggregate log lines from
different hosts and so there's a race condition. This program ignores this issue. To partially solve this, we could read
  multiple log lines at a time and sort them if needed.
