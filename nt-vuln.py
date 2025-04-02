import sys
import subprocess
import json
from pathlib import Path

def parseArgs():
    """Parse the arguments 
    Returns:
        - repo (string) : git repo to be scanned """
    # Parsing arguments
    if len(sys.argv) != 2:
        print("Please supply a git repo to scan")
        exit()

    repo = sys.argv[1]
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
    Returns:
        - repodir (pathlib.Path) : Working directory"""
    reponame = repoURL.split("/")[-1].removesuffix(".git")
    repodir = workdir / reponame
    # Pulling changes if the repo exists
    if repodir.exists():
        if repodir.is_dir():
            print("Repo directory already exists, pulling repo to get most recent version")
            try:
                res = subprocess.run(
                        f"cd {repodir} && git pull",                 
                        shell=True, 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to pull git repo.")
                print(e.stderr)
                exit()
        else:
            print("File with repo name exists. Please move")
            exit()
    else:
        # Repo does not exist, clone it
        print(f"Cloning repo {reponame}")
        try:
            res = subprocess.run(
                    f"cd {workdir} && git clone {repoURL}", 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone git repo. ")
            print(e.stderr)
            exit()

    # Check if the repos directory exists
    if not repodir.exists():
        print(f"Failed to clone git repo. Please provide a valid repository")
        print(res.stderr)
        exit()
 
    return repodir

def scanRepo(repodir):
    """Scan the provided repo using Trivy
    
    Parameters:
        - repodir (pathlib.Path) : Path of the repository to scan

    Returns:
        - results (dict) : dictionary containing the output of Trivy"""

    # Scan the repository
    try:
        res = subprocess.run(
                f"cd {repodir} && trivy fs --scanners vuln --format cyclonedx {repodir}", 
                shell=True, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)

    except subprocess.CalledProcessError as e:
        print(f"Failed to scan the repo. Please provide a valid repository")
        print(e.stderr)
        exit()

    # Convert the resulting json to a python dictionary
    try:
        results = json.loads(res.stdout)
    except:
        print("Failed to read Trivy output as JSON")
        print(res.stderr)
        exit()

    assert "vulnerabilities" in results, "Failed to read Trivy output as JSON"

    return results

def presentResults(scanResults):
    """Present the results from Trivy

    Parameters:
        - scanResults (dict) : Results from Trivy scan"""
    unrated = []
    rated = {}
    # Itterate through the vulnerabilities and find their hightst score
    # The rating key contains raitings, not all of which are CVSS ratings
    # Different sources can give different scores. Sort by the most severe rating
    for vulnerability in scanResults["vulnerabilities"]:
        maxscore = -1
        for rating in vulnerability["ratings"]:
            if "method" in rating:
                if "CVSS" in rating["method"]:
                    if "score" in rating:
                        if rating["score"] > maxscore:
                            maxscore = rating["score"]
        if maxscore == -1:
            # Seperate any vulnerabilities without any score
            unrated.append(vulnerability["id"])
        else:
            rated[vulnerability["id"]] = maxscore

    # Sorting the rated vulnerabilities
    rated = (sorted(rated.items(), key=lambda item: item[1]))[::-1]

    # Printing the results
    if len(rated) == 0:
        print("Trivey found no vulnerabilities with CVSS rating in the repo")
    else:
        print(f"Top {min(10, len(rated))} vulnerabilities:")
        for i in range(min( 10, len(rated))):
            print(f"{i+1:4} : {rated[i][0]:20} ({rated[i][1]} CVSS)")

    # Inform about vulnerabilities with no associated CVSS score
    if len(unrated) != 0:
        print(f"Trivy also found {len(unrated)} vulnerabilities with no associated CVSS score.")


if __name__ == "__main__":
    repoURL = parseArgs()
    wd = setupWorkDir()
    repodir = cloneRepo(repoURL, wd)
    trivyResults = scanRepo(repodir)
    presentResults(trivyResults)
