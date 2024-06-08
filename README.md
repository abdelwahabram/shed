# Shed
 - Another version control system

### Table of contents:
[About](#about)
- [Name origin](#name-origin)
- [Technologies](#technologies)
- [Demo](#demo)
- [Screenshots](#screenshots)
[Prerequisites](#prerequisites)
[Install](#install)
[Usage](#usage)
[License](#license)
[Contribution-guide](#contribution-guide)
[Contact-info](#contact)

### About:

#### Name origin:
Since this is more like a pythonic version of git, and Python is a family of snakes, the project is named after a biological process that happens in snakes called 'ecdysis' where the snake sheds its skin, to evolve and get rid of the parasites stuck to it comparing it with a developer extending his code and getting rid of the bugs.
#### Technologies:

 - Python
 - Click
#### Demo
- coming soon
#### Screenshots
### Prerequisites:
- Python 3.11

### Install
1. clone this repo
2. navigate to the repo directory
3. run `pip3 install -e .`
### Usage
1. `shed-create`: this command will create a shed repository
2. `shed-add [file/files]`: this command will add the specified file/s to be built
3. `shed-build [message]`: this command will build a shell(a.k.a git commit) of the tracked files
4. `shed-status`: print the repo current status to the stdout
5. `shed-delta`: prints the difference between the working directory and the under construction area(a.k.a index tree in git)
6. `shed-2-git`: this command creates the equivalent git repo of the current repository

### License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/abdelwahabram/shed/blob/main/LICENSE) for details.

### Contribution guide
1. Fork the project.
2. Create your feature branch (git checkout -b AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. to the branch (git push origin AmazingFeature).
5. Open a pull request.
if you want to report an issue follow this template:
## desired behavior:
- explanation
## actual behavior:
- explanation
## code reference:
[link if availabe]

### Contact
Abelwahab Abu Warda - abdelwahab.abu.warda610@gmail.com

