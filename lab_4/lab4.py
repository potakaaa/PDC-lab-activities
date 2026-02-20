import time

def handle_prompt(prompt):
    print("Prompt: ", prompt)
    print("Doing prompt...")
    time.sleep(5)

def handle_add(files):
    print("Adding files: ", files)
    print("Doing add...")
    time.sleep(3)

def handle_commit(files, message):
    pass

def handle_push(remote, branch):
    pass

def handle_create_pr(branch, title, desc):
    pass

def run_sequential():
    pass

def run_parallel():
    pass