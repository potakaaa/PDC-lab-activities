import time

def handle_prompt(prompt):
    print("Prompt: ", prompt)
    print("Doing prompt...")
    time.sleep(5)

def handle_add(files):
    print("Adding files: ", files)
    print("Doing add...")
    
    time.sleep(3)
    return files

def handle_commit(files, message):
    print("Committing files: ", files)
    print("Commit message: ", message)
    print("Doing commit...")
    time.sleep(1)

def handle_push(remote, branch):
    print("Pushing to remote: ", remote)
    print("Branch: ", branch)
    print("Doing push...")
    time.sleep(2)

def handle_create_pr(branch, title, desc):
    pass

def run_sequential():
    pass

def run_parallel():
    pass