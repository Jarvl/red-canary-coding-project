# Red Canary Coding Project

## Summary
I created an activity generator using Python 3.8.11 that will spawn a process, manipulate files, and initiate network requests while logging all activities. Logs are stored in a JSON format in order to balance human and machine readability, which can then be compared against an EDR agent for testing purposes.

## Activity Generation

When generating activities, slight delays are added to ensure that timestamps for each log are different from each other (and also for effect).

## Logging Activities

I designed the logging to prevent against a log entry being lost in the event of a crash/fatal error within the script. When an activity occurs, it's immediately logged, and the log file is subsequently closed (implicity by using a `with` block). When a new activity occurs, it is added to a running list of activity logs and the entire log file is rewritten using the full record of logs. This eliminates the need to parse the JSON log, adding the new activity to the resulting dictionary, and re-dumping the contents to the file, which may be less performant for large log files.

