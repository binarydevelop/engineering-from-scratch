# Exercise Set 03: Text Processing Mastery

### Ex 3.1: Grep Inverting & Counting
In a sample web server log, count the exact number of requests that did NOT return HTTP status `200` without displaying the matching lines.

### Ex 3.2: Regex Extraction with Egrep
Using `grep -E`, extract all valid IPv4 addresses from `/etc/hosts` and `/var/log/syslog`.

### Ex 3.3: Case-Insensitive Recursive Search
Search recursively through `/etc` for the string `PermitRootLogin`, displaying the matching file path, line number, and matching content, suppressing permission errors.

### Ex 3.4: Stream Editing: In-Place Safe Replacement
Using `sed`, replace every occurrence of port `8080` with port `9090` in a configuration file, creating an automatic `.bak` backup file in the process.

### Ex 3.5: Sed Address Ranges
Using `sed`, print only lines 15 through 35 of a 100-line log file without using `head` or `tail`.

### Ex 3.6: Sed Line Deletion
Using `sed`, delete all blank lines and all comment lines (lines beginning with `#`, ignoring leading whitespace) from a configuration file.

### Ex 3.7: Awk Column Extraction
Given `/etc/passwd`, use `awk` to print only the username (field 1) and user shell (field 7), formatted in neatly aligned columns separated by a tab.

### Ex 3.8: Awk Filtering by Numeric Threshold
Using `awk`, process `/etc/passwd` to display only user accounts whose numeric UID is greater than or equal to `1000` but excluding user `nobody` (UID 65534).

### Ex 3.9: Awk Summation & Averages
Using `ls -l /var/log`, write a one-line `awk` script that calculates and prints the total sum in megabytes of all regular files in the directory.

### Ex 3.10: Sort by Numeric Key
Given a space-delimited table of process metrics, sort the output in descending numerical order based on the 3rd column (CPU utilization).

### Ex 3.11: Finding Unique IP Frequencies
Given a simulated web access log, extract the client IP address (column 1), sort them, and display the top 5 most frequent client IPs alongside their exact hit counts.

### Ex 3.12: Cut Field Extraction
Using `cut`, extract the second and fourth fields of a comma-separated CSV file without invoking `awk`.

### Ex 3.13: Tr Character Translation & Deletion
Use `tr` to convert a lowercase text stream to uppercase, and then use `tr -d` to strip all Windows carriage return characters (`\r`) from a DOS text file.

### Ex 3.14: Line, Word, and Byte Auditing with WC
Write a command to count the exact number of user accounts configured on the system that have `/bin/bash` as their default login shell.

### Ex 3.15: Combining the Pipeline
Construct a single composite pipeline: read `/var/log/auth.log` (or systemd auth journal), extract failed SSH login attempts, parse the offending usernames, count their frequency, and sort by highest failure count.
