# Exercise Set 10: Defensive Bash Scripting

### Ex 10.1: The Defensive Preamble
Explain the exact failure modes prevented by `set -euo pipefail` in production Bash scripts:
- What does `-e` do, and when does it silently fail?
- What does `-u` do?
- What does `-o pipefail` do?

### Ex 10.2: Safe Variable Quoting
Demonstrate a scenario where an unquoted variable `$FILE` causes a script to delete the wrong files or split on whitespace.

### Ex 10.3: Exit Codes and Conditional Execution
Write a Bash snippet that tests whether a directory exists, creates it if missing, and exits with code 1 if directory creation fails, using `&&` and `||`.

### Ex 10.4: Safe Iteration Over Files
Write a `for` loop that iterates over all `.log` files in a directory safely without parsing `ls` or failing when no matching files exist (`shopt -s nullglob`).

### Ex 10.5: Processing Input Line by Line
Write a `while IFS= read -r line` loop that safely reads a text file line-by-line, preserving leading and trailing whitespace and handling files lacking a trailing newline.

### Ex 10.6: Bash Script Arguments and Shifts
Write a script that accepts command-line flags (`-u <user>`, `-d <dir>`, `-h`), validates required arguments, and handles unexpected inputs with a clear usage message.

### Ex 10.7: Trap for Guaranteed Resource Cleanup
Write a Bash script that creates a temporary directory using `mktemp -d`. Register an `EXIT` trap (`trap 'rm -rf "$TMP_DIR"' EXIT`) to guarantee deletion even if the script is interrupted by `Ctrl-C` or errors out.

### Ex 10.8: Bash Functions and Local Scope
Write a reusable Bash function that calculates disk usage percentage. Ensure all internal variables are declared with `local` to prevent namespace pollution.

### Ex 10.9: Integer Arithmetic vs External Tools
Demonstrate how to perform integer math in native Bash using `$(( a + b ))` without spawning slow subshells running `expr` or `bc`.

### Ex 10.10: String Manipulation Without Sed/Awk
Use native Bash parameter expansion to extract: the file extension (`${FILE##*.}`), the filename without extension (`${FILE%.*}`), and string replacement (`${VAR//foo/bar}`).

### Ex 10.11: Atomic Locking with Flock
Write a cron-compatible Bash wrapper that uses `flock` to prevent multiple concurrent instances of the same script from running simultaneously.

### Ex 10.12: ShellCheck Linting
Take a poorly written shell script containing unquoted variables, useless `cat` usage, and unhandled errors. Run `shellcheck` and refactor the script into a clean, defensive production utility.
