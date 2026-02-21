"""
Git workflow agent simulation with loading animations and agent-style output.

This module simulates a git workflow agent that processes user prompts,
stages files, creates commits, pushes to remote, and opens pull requests.
Supports both sequential and parallel execution modes with optional
buffered output for thread-safe printing.
"""
import sys
import threading
import time
from typing import Optional

# Braille pattern spinner frames for smooth animation
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
SPINNER_INTERVAL = 0.08  # Seconds between spinner frame updates

# Lock for atomic printing of buffered agent output in parallel mode
_print_lock = threading.Lock()


def _spinner_worker(stop_event: threading.Event, message: str) -> None:
    """
    Run a Braille-pattern spinner animation in a background thread.

    Displays a rotating spinner with the given message until the stop_event
    is set. Clears the line on exit to avoid leaving artifacts.

    Args:
        stop_event: Event that signals the spinner to stop when set.
        message: Text to display alongside the spinner (e.g., "Loading...").
    """
    idx = 0
    while not stop_event.is_set():
        frame = SPINNER_FRAMES[idx % len(SPINNER_FRAMES)]
        sys.stdout.write(f"\r  {frame}  {message}")
        sys.stdout.flush()
        idx += 1
        stop_event.wait(SPINNER_INTERVAL)
    sys.stdout.write("\r" + " " * (len(message) + 8) + "\r")
    sys.stdout.flush()


def run_with_loading(
    duration: float,
    message: str,
    output_buffer: Optional[list[str]] = None,
) -> None:
    """
    Execute a timed operation with an optional loading spinner.

    In interactive mode (output_buffer is None), starts a background thread
    that displays a spinner for the given duration. In buffered mode, records
    a static loading message and sleeps without animation.

    Args:
        duration: How long to run the simulated operation (seconds).
        message: Loading message shown during the operation.
        output_buffer: If provided, output is appended here instead of
            displaying a live spinner. Used for parallel execution.
    """
    if output_buffer is not None:
        output_buffer.append(f"   ⏳  {message}\n")
        time.sleep(duration)
        return
    stop_event = threading.Event()
    spinner = threading.Thread(
        target=_spinner_worker,
        args=(stop_event, message),
        daemon=True,
    )
    spinner.start()
    time.sleep(duration)
    stop_event.set()
    spinner.join(timeout=0.5)


def _agent_header(title: str, output_buffer: Optional[list[str]] = None) -> None:
    """
    Print a styled box header for an agent task section.

    Renders a bordered header with a bullet and title (e.g., "STAGING FILES").

    Args:
        title: The section title to display in the header.
        output_buffer: If provided, lines are appended here instead of
            printing to stdout.
    """
    width = 52
    lines = [
        f"\n┌{'─' * (width - 2)}┐",
        f"│  ●  {title:<{width - 8}}│",
        f"└{'─' * (width - 2)}┘",
    ]
    if output_buffer is not None:
        output_buffer.extend(line + "\n" for line in lines)
    else:
        for line in lines:
            print(line)


def _agent_line(
    label: str,
    value: str,
    output_buffer: Optional[list[str]] = None,
) -> None:
    """
    Print a formatted key-value info line in agent output style.

    Renders a line like "   →  Label: value" for structured output.

    Args:
        label: The field name (e.g., "Files", "Message").
        value: The field value to display.
        output_buffer: If provided, the line is appended here instead of
            printing to stdout.
    """
    line = f"   →  {label}: {value}"
    if output_buffer is not None:
        output_buffer.append(line + "\n")
    else:
        print(line)


def _agent_success(
    message: str,
    output_buffer: Optional[list[str]] = None,
) -> None:
    """
    Print a success completion message with a checkmark prefix.

    Renders a line like "   ✓  message" to indicate task completion.

    Args:
        message: The success message to display.
        output_buffer: If provided, the line is appended here instead of
            printing to stdout.
    """
    line = f"   ✓  {message}\n"
    if output_buffer is not None:
        output_buffer.append(line)
    else:
        print(line)


def handle_prompt(
    prompt: str,
    output_buffer: Optional[list[str]] = None,
) -> None:
    """
    Process and simulate analysis of the user's git workflow prompt.

    Displays a "PROMPT ANALYSIS" section, shows the input prompt, runs a
    simulated loading phase, and reports success. Used as the first step
    in the agent pipeline.

    Args:
        prompt: The user's natural language prompt (e.g., "Fix bug in login").
        output_buffer: If provided, output is appended here instead of
            printing to stdout.
    """
    _agent_header("PROMPT ANALYSIS", output_buffer)
    _agent_line("Input", prompt, output_buffer)
    _emit("\n", output_buffer)
    run_with_loading(
        5,
        "Analyzing intent and planning workflow...",
        output_buffer,
    )
    _agent_success("Prompt understood. Workflow initialized.", output_buffer)


def handle_add(
    files: list[str],
    output_buffer: Optional[list[str]] = None,
) -> list[str]:
    """
    Simulate staging files for commit (git add).

    Displays a "STAGING FILES" section, lists the files being staged, runs
    a simulated loading phase, and reports success. Returns the same file
    list for chaining with handle_commit.

    Args:
        files: List of file paths to stage (e.g., ["login.py", "utils.py"]).
        output_buffer: If provided, output is appended here instead of
            printing to stdout.

    Returns:
        The same list of files that were staged, for pipeline chaining.
    """
    _agent_header("STAGING FILES", output_buffer)
    _agent_line("Files", ", ".join(files), output_buffer)
    _emit("\n", output_buffer)
    run_with_loading(3, "Staging files to index...", output_buffer)
    _agent_success(f"Staged {len(files)} file(s) successfully.", output_buffer)
    return files


def handle_commit(
    files: list[str],
    message: str,
    output_buffer: Optional[list[str]] = None,
) -> None:
    """
    Simulate creating a commit with the staged files (git commit).

    Displays a "CREATING COMMIT" section with files and message, runs a
    simulated loading phase, and reports success.

    Args:
        files: List of file paths included in the commit.
        message: The commit message (e.g., "Fixed login bug").
        output_buffer: If provided, output is appended here instead of
            printing to stdout.
    """
    _agent_header("CREATING COMMIT", output_buffer)
    _agent_line("Files", ", ".join(files), output_buffer)
    _agent_line("Message", message, output_buffer)
    _emit("\n", output_buffer)
    run_with_loading(1, "Writing commit to repository...", output_buffer)
    _agent_success("Commit created successfully.", output_buffer)


def handle_push(
    remote: str,
    branch: str,
    output_buffer: Optional[list[str]] = None,
) -> str:
    """
    Simulate pushing commits to a remote repository (git push).

    Displays a "PUSHING TO REMOTE" section with remote and branch, runs a
    simulated loading phase, and reports success. Returns the branch name
    for chaining with handle_create_pr.

    Args:
        remote: Remote name (e.g., "origin").
        branch: Branch name to push (e.g., "fix/login").
        output_buffer: If provided, output is appended here instead of
            printing to stdout.

    Returns:
        The branch name that was pushed, for pipeline chaining.
    """
    _agent_header("PUSHING TO REMOTE", output_buffer)
    _agent_line("Remote", remote, output_buffer)
    _agent_line("Branch", branch, output_buffer)
    _emit("\n", output_buffer)
    run_with_loading(2, "Uploading commits to remote...", output_buffer)
    _agent_success(f"Pushed to {remote}/{branch}.", output_buffer)
    return branch


def handle_create_pr(
    branch: str,
    title: str,
    desc: str,
    output_buffer: Optional[list[str]] = None,
) -> str:
    """
    Simulate creating a pull request from a branch.

    Displays a "CREATING PULL REQUEST" section with branch, title, and a
    truncated description, runs a simulated loading phase, and reports
    success. Returns the branch name.

    Args:
        branch: Source branch for the PR (e.g., "fix/login").
        title: PR title (e.g., "Fix Login").
        desc: PR description; displayed truncated to 40 chars if longer.
        output_buffer: If provided, output is appended here instead of
            printing to stdout.

    Returns:
        The branch name associated with the created PR.
    """
    _agent_header("CREATING PULL REQUEST", output_buffer)
    _agent_line("Branch", branch, output_buffer)
    _agent_line("Title", title, output_buffer)
    desc_preview = (desc[:40] + "...") if len(desc) > 40 else desc
    _agent_line("Description", desc_preview, output_buffer)
    _emit("\n", output_buffer)
    run_with_loading(3, "Opening pull request...", output_buffer)
    _agent_success("Pull request created successfully.", output_buffer)
    return branch


def _emit(text: str, output_buffer: Optional[list[str]]) -> None:
    """
    Emit raw text to an output buffer or stdout.

    Used internally for consistent output routing across the agent pipeline.
    When output_buffer is provided, appends text without a trailing newline
    (caller controls formatting). When None, prints to stdout.

    Args:
        text: The raw text to emit (may include newlines).
        output_buffer: If provided, text is appended here. If None, prints
            to stdout with end="" to preserve caller-controlled newlines.
    """
    if output_buffer is not None:
        output_buffer.append(text)
    else:
        print(text, end="")


def run_agent(
    prompt: str,
    files: list[str],
    message: str,
    remote: str,
    branch: str,
    title: str,
    desc: str,
    output_buffer: Optional[list[str]] = None,
) -> None:
    """
    Execute the full git workflow agent pipeline for a single task.

    Runs the complete simulated workflow: prompt analysis → stage files →
    commit → push → create PR. Output can be printed directly or buffered
    for thread-safe parallel execution.

    Args:
        prompt: User's natural language prompt describing the task.
        files: List of file paths to stage and commit.
        message: Commit message.
        remote: Remote repository name (e.g., "origin").
        branch: Branch name for push and PR.
        title: Pull request title.
        desc: Pull request description.
        output_buffer: If provided, all output is appended here instead of
            printing. Use for parallel mode to avoid interleaved output.
    """
    _emit("\n" + "═" * 52 + "\n", output_buffer)
    _emit("  🤖  GIT WORKFLOW AGENT — STARTING\n", output_buffer)
    _emit("═" * 52 + "\n", output_buffer)

    handle_prompt(prompt, output_buffer)
    handle_commit(
        handle_add(files, output_buffer),
        message,
        output_buffer,
    )
    handle_create_pr(
        handle_push(remote, branch, output_buffer),
        title,
        desc,
        output_buffer,
    )

    _emit("═" * 52 + "\n", output_buffer)
    _emit("  ✓  AGENT COMPLETE — All tasks finished successfully\n", output_buffer)
    _emit("═" * 52 + "\n\n", output_buffer)


# Predefined workflow tasks for sequential/parallel execution demos
tasks = [
    {
        "prompt": "Fix bug in login",
        "files": ["login.py"],
        "message": "Fixed login bug",
        "remote": "origin",
        "branch": "fix/login",
        "title": "Fix Login",
        "desc": "Fixed the login bug"
    },
    {
        "prompt": "Add feature X",
        "files": ["feature.py"],
        "message": "Added feature X",
        "remote": "origin",
        "branch": "feat/x",
        "title": "Feature X",
        "desc": "Added feature X"
    },
    {
        "prompt": "Update documentation",
        "files": ["README.md"],
        "message": "Updated README",
        "remote": "origin",
        "branch": "docs/update",
        "title": "Update Docs",
        "desc": "Updated valid documentation"
    },
    {
        "prompt": "Refactor database",
        "files": ["db.py"],
        "message": "Refactored DB",
        "remote": "origin",
        "branch": "refactor/db",
        "title": "Refactor DB",
        "desc": "Refactored database connection"
    }
]

def run_sequential() -> float:
    """
    Run the agent workflow for all tasks sequentially.

    Executes each task in tasks one after another, printing output directly
    to stdout. Used to compare baseline performance against parallel mode.

    Returns:
        Total execution time in seconds (float).
    """
    start_time = time.time()
    for task in tasks:
        run_agent(**task)
    return time.time() - start_time


def _run_agent_buffered(task: dict) -> None:
    """
    Run the agent for one task with buffered output, then print atomically.

    Executes run_agent with output_buffer to capture all output, then
    acquires _print_lock and prints the buffer in one block. Ensures
    each task's output appears contiguously in parallel execution.

    Args:
        task: Dict with keys prompt, files, message, remote, branch,
            title, desc. Passed as **task to run_agent.
    """
    buffer: list[str] = []
    run_agent(**task, output_buffer=buffer)
    with _print_lock:
        for line in buffer:
            print(line, end="")


def run_parallel() -> float:
    """
    Run the agent workflow for all tasks in parallel using threads.

    Spawns one thread per task. Each thread buffers its output and prints
    atomically under _print_lock to avoid interleaved output. Used to
    demonstrate parallel execution speedup.

    Returns:
        Total execution time in seconds (float).
    """
    start_time = time.time()
    threads = []

    for task in tasks:
        thread = threading.Thread(target=_run_agent_buffered, args=(task,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return time.time() - start_time


if __name__ == "__main__":
    print("Running sequential execution...")
    seq_time = run_sequential()

    print("\n" + "=" * 60 + "\n")

    print("Running parallel execution...")
    par_time = run_parallel()

    print(f"\nSequential execution time: {seq_time:.2f} seconds")
    print(f"Parallel execution time: {par_time:.2f} seconds")
