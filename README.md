# nt-vuln
Wrapper tool for Trivy
Clone git repo and get a list of the most severe vulnerabilities discovered by trivy in the project.

## Requirements
To use this tool, you need to have git, Trivy and python 3 installed.
Install trivy: https://trivy.dev/latest/getting-started/installation/
Install git: https://git-scm.com/downloads

## Known issues
The tool assumes that a pre-existing folder with the repo name is the repo that is being cloned.
Thus checking two repos with equeal names will actually only check the first repo twise.
