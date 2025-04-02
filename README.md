# nt-vuln
Get a list of the most severe vulnerabilities discovered by Trivy in a git repo.
This is a wrapper tool for Trivy.

## Requirements
To use this tool, you need to have git, Trivy and python 3 installed.
Install trivy: https://trivy.dev/latest/getting-started/installation/
Install git: https://git-scm.com/downloads

## Usage
To use the tool, install the requirements, download the script nt-vuln.py or clone the repo.
Navigate to the folder containing the script, and run it with the url of the git repo:
```bash
$ python3 nt-vuln.py [git repo]
```
Example usage on this project:
```bash
$ python3 nt-vuln.py https://github.com/luterlassus/nt-vuln
```

## Known issues
The tool assumes that a pre-existing folder in the ~/.nt-vuln directory with the repo name is the repo that is being cloned.
Thus checking two repos with equeal names will actually only check the first repo twise.
If you know this is the case, remove the first repos folder from ~/.nt-vuln before the second run of the tool.

## Improvements
Possible improvements includes 
* Fixing the git folder name collision senario described above by verifying that the projects are the same.
* Implementing better argument parsing to allow for more or less verbose output, specifying number of vulnerabilities to print, user specified work directory etc. 
* Using more nt-vuln scanners or tools to get more information.
* Automatic cleanup if specified by user.

## Limitations
This tool uses Trivy to scan for vulnerabilities.
It uses the vuln scanner, which looks for vulnerabilities based on lock files such as package-lock.json.
Hence, such files must be included in the project for this tool to work. 
The tool does not use the other scanners, and there is no guarantee that all vulnerabilities are found,
and neither that the found vulnerabilites are actually exploitable in the repo. 
