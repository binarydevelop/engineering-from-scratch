# Exercise Set 02: Pipes & Redirection

### Ex 2.1: Separating Streams
Run a command that writes output to both `stdout` (FD 1) and `stderr` (FD 2). Redirect `stdout` to `/tmp/lfs-lab/out.log` and `stderr` to `/tmp/lfs-lab/err.log` simultaneously.

### Ex 2.2: Merging Diagnostic Streams
Execute a command that fails, redirecting both standard output and standard error into a single unified log file `/tmp/lfs-lab/combined.log` using modern Bash syntax.

### Ex 2.3: Discarding Noise Completely
Run a verbose system command while discarding all diagnostic error output (`stderr`) into the Linux null character device `/dev/null` while preserving standard output in your terminal.

### Ex 2.4: Append vs Truncate Hazard
Explain the difference between `>` and `>>`. Demonstrate how a misconfigured monitoring script using `>` will corrupt an existing historical audit log.

### Ex 2.5: The Tee Diagnostic Tap
Construct a pipeline where output from a command is displayed on your terminal screen in real time while simultaneously being appended to a persistent disk file.

### Ex 2.6: Input Redirection via Here-Doc
Write a command using a multi-line Bash Here-Doc (`<< 'EOF'`) that writes a multi-line configuration file directly to disk without opening an interactive editor.

### Ex 2.7: Heredoc with Variable Interpolation
Demonstrate the difference between `<< EOF` and `<< 'EOF'`. Show how unquoted EOF evaluates `$HOSTNAME` and `$UID` during file generation, while quoted `'EOF'` preserves the literal string.

### Ex 2.8: Pipeline Exit Codes and PIPESTATUS
In the pipeline `false | true | cat`, what is the exit status in `$?`? How do you inspect the exit code of the failed first command using Bash's internal `${PIPESTATUS[@]}` array?

### Ex 2.9: Process Substitution
Compare the output of two directories (`/etc/pam.d` and `/etc/security`) using `diff` without creating any temporary files on disk, utilizing Bash process substitution `<(...)`.

### Ex 2.10: Custom File Descriptors
Open file descriptor 3 for writing to `/tmp/lfs-lab/custom.log` inside your current shell session. Write three distinct log messages to FD 3, and then close FD 3 cleanly.
