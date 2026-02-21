import time

def handle_prompt(prompt):
    print("Prompt: ", prompt)
    print("Doing prompt...\n")
    time.sleep(5)

def handle_add(files):
    print("Adding files: ", files)
    print("Doing add...\n")
    
    time.sleep(3)
    return files

def handle_commit(files, message):
    print("Committing files: ", files)
    print("Commit message: ", message)
    print("Doing commit...\n")
    time.sleep(1)

def handle_push(remote, branch):
    print("Pushing to remote: ", remote)
    print("Branch: ", branch)
    print("Doing push...\n")
    time.sleep(2)
    return branch

def handle_create_pr(branch, title, desc):
    print("Title: ", title)
    print("Description: ", desc)
    print("Creating PR...\n")
    time.sleep(3)
    return branch


def run_agent(task):
    handle_prompt(task["prompt"])
    handle_commit(handle_add(task["files"]), task["message"])
    handle_create_pr(handle_push(task["remote"], task["branch"]), task["title"], task["desc"])

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

def run_sequential():
    start_time = time.time()
    for task in tasks:
        run_agent(task)
    end_time = time.time()
    print(f"Sequential execution time: {end_time - start_time:.2f} seconds")

def run_parallel():
    pass