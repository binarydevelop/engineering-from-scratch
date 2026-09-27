# Capstone 1: Expanded Unix Shell (`mini-shell`)

> **Motto:** The shell is not an operating system; it is an ordinary userspace process that transforms textual commands into kernel process creation (`fork`), program replacement (`exec`), and descriptor manipulation (`dup2`).

---

## 1. Architectural Overview

The shell operates in a continuous read-eval-print loop (REPL):
1. **Read:** Reads a line of input from `stdin` (`fgets`).
2. **Parse:** Tokenizes the command string into executable arguments and identifies control operators (`|`, `>`, `>>`, `<`, `&`).
3. **Built-in Dispatch:** Checks if the command is implemented directly inside the shell process (`cd`, `pwd`, `help`, `exit`).
4. **Process Forking:** Invokes `fork()` to create an isolated child process.
5. **Descriptor Redirection:** Rewires `stdin` or `stdout` using `dup2()` if redirection operators were specified.
6. **Program Replacement:** Calls `execvp()` to load the new binary into the child's address space.
7. **Lifecycle Synchronization:** Calls `waitpid()` in the parent process to wait for the child and reap its zombie state.

---

## 2. Compiling and Running

```bash
make
./mini-shell
```

### Supported Commands & Syntax

#### 1. Basic Execution
```bash
mini-shell> ls -la
mini-shell> echo "Hello from mini-shell"
```

#### 2. Built-in Commands
```bash
mini-shell> pwd
mini-shell> cd ..
mini-shell> pwd
```

#### 3. Output & Input Redirection
```bash
mini-shell> echo "Writing to file" > test_output.txt
mini-shell> cat < test_output.txt
mini-shell> echo "Appending line" >> test_output.txt
mini-shell> cat test_output.txt
```

#### 4. Pipelines
```bash
mini-shell> ls -l | grep txt
mini-shell> ps | grep mini
```

#### 5. Background Jobs
```bash
mini-shell> sleep 2 &
```
