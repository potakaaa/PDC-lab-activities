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


def run_agent(prompt, files, message, remote, branch, title, desc):
    handle_prompt(prompt)
    handle_commit(handle_add(files), message)
    handle_create_pr(handle_push(remote, branch), title, desc)

run_agent("do something", ["file1.txt", "file2.txt"], "commit message", "origin", "main", "title", "description")

def run_sequential():
    pass

def run_parallel():
    pass