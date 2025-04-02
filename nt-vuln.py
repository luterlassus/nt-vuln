import sys
from pathlib import Path
import subprocess

def parseArgs():
    """Parse the arguments 
    Returns:
        - repo (string) : git repo to be scanned """
    # Parsing arguments
    if len(sys.argv) != 2:
        print("Please supply a git repo to scan")
        exit()

    repo = sys.argv[1]
    print(f"Downloading the provided repo {repo}")
    return repo

def setupWorkDir():
    """Setup the working directory of the tool 
    Returns:
        - workdir (pathlib.Path) : Path of working directory"""
    # Finding the working directory
    workdir = Path.home() / ".nt-vuln"
    if workdir.exists():
        # ~/.nt-vuln exists
        if not workdir.is_dir():
            print("~/.nt-vuln exists, but is not a directory \nPlease move it before using this tool")
            exit()
    else:
        print("Creating nt-vuln directory in home dir")
        workdir.mkdir()

    return workdir

def cloneRepo(repoURL, workdir):
    """Clone the provided repo into the working directory. 
    Pull changes if repo directory already exists.

    Parameters:
        - repoURL (string) : URL of repo to be cloned
        - workdir (pathlib.Path) : Working directory
    Returns
        - repodir (pathlib.Path) : Working directory"""
    reponame = repoURL.split("/")[-1].strip(".git")
    repodir = workdir / reponame
    # Pulling changes if the repo exists
    if repodir.exists():
        if repodir.is_dir():
            print("Repo directory already exists, pulling repo")
            try:
                res = subprocess.check_output(f"cd {repodir} && git pull", shell=True)
                print(f"Res : {res}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to clone git repo. Please provide a valid repository")
        else:
            print("File with repo name exists. Please move")
            exit()
    else:
        # Repo does not exist, clone it
        print(f"Cloning repo {reponame}")
        try:
            res = subprocess.check_output(f"cd {workdir} && git clone {repoURL}", shell=True)
            print(f"Res : {res}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone git repo. Please provide a valid repository")

if __name__ == "__main__":
    repoURL = parseArgs()
    wd = setupWorkDir()
    cloneRepo(repoURL, wd)
