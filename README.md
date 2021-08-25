# Red Canary Coding Project

## Summary

I created an activity generator using Python 3.8 that will spawn a process, manipulate files, and initiate network requests while logging all activities to a user-defined log file. Logs are stored in a YAML format in order to balance readability and performance, which can then be compared against an EDR agent for testing purposes. Most data behind activities is configurable via the application's command-line arguments. This application is also fitted with automated unit tests for proper test coverage.

## Compatibility

MacOS and Linux (it _should_ also be compatible with Windows, although I am unable to test)

## Setup

Ensure that Python 3.8 is installed

This project uses [pipenv](https://github.com/pypa/pipenv) for virtual env/package management, it's recommended to install that first. Alternatively, the packages within `Pipfile` can be installed manually.

After installing pipenv, run `pipenv install` to install packages.

## Example Usage

Running the application and generating logs
```bash
pipenv run python main.py --log-file-path logs/activity_log.yaml --test-file-path test.txt --test-command "ls -al" --test-hostname www.google.com --test-port 80
```

Running unit tests
```bash
pipenv run python -m unittest
```

## How it works

This application contains most of its logic inside of the `activity_generator` package within two classes: `Generator` and `Logger`. The `Generator` class has methods for the types of activities that can be triggered by the application, such as file creation/modification/deletion, starting a process, and transmitting data. `Logger` handles all of the logic for compiling data around an activity and appending it to a log file.

All activity logs contain a unix timestamp and data around the process that triggered the activity. In most cases, this process data is the activity generator application, but this differs for a triggered process activity (see below).

### File Activities

The filename for triggering a file activity is configurable via the `--test-file-path` command-line argument. The filename can be relative, and will be converted to an full/absolute path for logging purposes. This activity logs relevant file data and data about the process currently manipulating the files.

### Process Activity

The executable for triggering a process activity is configurable via the `--test-command` command-line argument. The executable and its arguments/flags are defined as a single string to mimic how a command would normally be executed in the command-line (e.g. `ls -al`). This can also be leveraged to automate commands to used for testing if desired. This activity logs the start time and other data about the newly launched process, as opposed to the activity generator process.

## Network Activities

The hostname and port for triggering a network activity is configurable via the `--test-hostname` and `--test-port` command-line arguments. Network activities will log the activity generator process data, as well as data about the socket connection and data transmitted during it (source/destination IP and port, bytes sent, protocol). Note that the log entry for a network connection protocol will always be `tcp`. Making this dynamic could be a possible feature for the future.

## Notes on Logging

I designed the logging to prevent against a log entry being lost in the event of a crash/fatal error within the script. When an activity occurs, it's immediately logged, and the log file is subsequently closed (implicitly by using a `with` block). When a new activity occurs, it is appended to the log file immediately. Logging this way (i.e. only appending logs) means that my code can manipulate very large log files, since it does not require parsing the log contents before writing additional ones. This is the main reason why I chose YAML as a log format.

## Notes on Testing

Much of the testing in this application leverages mocking. This is especially important for `open()` calls where it's disadvantageous to create persistent files on disk during a unit test. Mocking file manipulation, while it's more verbose, results in a bit more performant code and prevents lingering test files (in case they're never deleted).

I also wrote the unit tests in a way where the tests for `Generator` and `Logger` do not overlap. `Generator` unit tests use a mock `Logger` instance to log activities, so the logging code is never called within these unit tests. This saves from mocking underlying logging functionality for every test which can result in bloated tests, and lack of seperation of concerns.