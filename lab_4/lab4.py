"""
Git workflow agent simulation with loading animations and agent-style output.
"""
import sys
import threading
import time

# Braille pattern spinner frames for smooth animation
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
SPINNER_INTERVAL = 0.08


def _spinner_worker(stop_event: threading.Event, message: str) -> None:
    """Run spinner animation until stop_event is set."""
    idx = 0
    while not stop_event.is_set():
        frame = SPINNER_FRAMES[idx % len(SPINNER_FRAMES)]
        sys.stdout.write(f"\r  {frame}  {message}")
        sys.stdout.flush()
        idx += 1
        stop_event.wait(SPINNER_INTERVAL)
    sys.stdout.write("\r" + " " * (len(message) + 8) + "\r")
    sys.stdout.flush()


def run_with_loading(duration: float, message: str) -> None:
    """Execute a timed operation with a loading spinner."""
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


def _agent_header(title: str) -> None:
    """Print a styled agent task header."""
    width = 52
    print(f"\n┌{'─' * (width - 2)}┐")
    print(f"│  ●  {title:<{width - 8}}│")
    print(f"└{'─' * (width - 2)}┘")


def _agent_line(label: str, value: str) -> None:
    """Print a formatted agent info line."""
    print(f"   →  {label}: {value}")


def _agent_success(message: str) -> None:
    """Print a success completion message."""
    print(f"   ✓  {message}\n")


def handle_prompt(prompt: str) -> None:
    """Process and analyze the user prompt."""
    _agent_header("PROMPT ANALYSIS")
    _agent_line("Input", prompt)
    print()
    run_with_loading(5, "Analyzing intent and planning workflow...")
    _agent_success("Prompt understood. Workflow initialized.")


def handle_add(files: list[str]) -> list[str]:
    """Stage files for commit."""
    _agent_header("STAGING FILES")
    _agent_line("Files", ", ".join(files))
    print()
    run_with_loading(3, "Staging files to index...")
    _agent_success(f"Staged {len(files)} file(s) successfully.")
    return files


def handle_commit(files: list[str], message: str) -> None:
    """Create a commit with the staged files."""
    _agent_header("CREATING COMMIT")
    _agent_line("Files", ", ".join(files))
    _agent_line("Message", message)
    print()
    run_with_loading(1, "Writing commit to repository...")
    _agent_success("Commit created successfully.")


def handle_push(remote: str, branch: str) -> str:
    """Push commits to remote repository."""
    _agent_header("PUSHING TO REMOTE")
    _agent_line("Remote", remote)
    _agent_line("Branch", branch)
    print()
    run_with_loading(2, "Uploading commits to remote...")
    _agent_success(f"Pushed to {remote}/{branch}.")
    return branch


def handle_create_pr(branch: str, title: str, desc: str) -> str:
    """Create a pull request."""
    _agent_header("CREATING PULL REQUEST")
    _agent_line("Branch", branch)
    _agent_line("Title", title)
    desc_preview = (desc[:40] + "...") if len(desc) > 40 else desc
    _agent_line("Description", desc_preview)
    print()
    run_with_loading(3, "Opening pull request...")
    _agent_success("Pull request created successfully.")
    return branch


def run_agent(
    prompt: str,
    files: list[str],
    message: str,
    remote: str,
    branch: str,
    title: str,
    desc: str,
) -> None:
    """Execute the full git workflow agent pipeline."""
    print("\n" + "═" * 52)
    print("  🤖  GIT WORKFLOW AGENT — STARTING")
    print("═" * 52)

    handle_prompt(prompt)
    handle_commit(handle_add(files), message)
    handle_create_pr(handle_push(remote, branch), title, desc)

    print("═" * 52)
    print("  ✓  AGENT COMPLETE — All tasks finished successfully")
    print("═" * 52 + "\n")


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

def run_sequential() -> None:
    """Run agent workflow sequentially."""
    start_time = time.time()
    for task in tasks:
        run_agent(**task)
    end_time = time.time()
    print(f"Sequential execution time: {end_time - start_time:.2f} seconds")


def run_parallel() -> None:
    """Run agent workflow in parallel."""
    start_time = time.time()
    threads = []
    
    for task in tasks:
        thread = threading.Thread(target=run_agent, kwargs=task)
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    end_time = time.time()
    print(f"Parallel execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    print("Running sequential execution...")
    run_sequential()
    
    print("\n" + "="*60 + "\n")
    
    print("Running parallel execution...")
    run_parallel()
