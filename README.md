# Red Canary Coding Project

## Summary
I created an activity generator using Python 3.8.11 that will spawn a process, manipulate files, and initiate network requests while logging all activities. Logs are stored in a YAML format in order to balance readability and performance, which can then be compared against an EDR agent for testing purposes.

## Activity Generation

When generating activities, slight delays are added to ensure that timestamps for each log are different from each other (and also for effect).

## Logging Activities

I designed the logging to prevent against a log entry being lost in the event of a crash/fatal error within the script. When an activity occurs, it's immediately logged, and the log file is subsequently closed (implicity by using a `with` block). When a new activity occurs, it is appended to the log file immediately. Logging this way (i.e. only appending logs) means that my code can manipulate very large log files, since it does not require parsing the log contents before writing additional ones. This is also one of the reasons I chose YAML as a log format.

