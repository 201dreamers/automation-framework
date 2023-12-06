## Installation and Configuration Instructions:

## Table of Contents

- [Installation and Configuration Instructions:](#installation-and-configuration-instructions)
  - [General Functionality Overview](#general-functionality-overview)
    - [Related docs to read:](#related-docs-to-read)
    - [Project structure](#project-structure)
  - [Cloning the Repository using SSH:](#cloning-the-repository-using-ssh)
- [Storing Sensitive Data](#storing-sensitive-data)
- [Creating a Virtual Environment and Installing Dependencies](#creating-a-virtual-environment-and-installing-dependencies)


### General Functionality Overview
This instruction covers a framework based on "pytest," which is the foundation of this repository. "Pytest" is a tool for automated software testing in general. The framework developed herein is built on top of it and includes a set of functional capabilities to simplify testing and integration with testing devices.

The system has a well-defined file structure and provides core functionalities for interacting with testing devices.

#### Related docs to read:
- [Code Formatting](https://github.com/201dreamers/automation-framework/blob/main/docs/code_formatting.md)
- [Reporting](https://github.com/201dreamers/automation-framework/blob/main/docs/reporting.md)
- [Running Tests](https://github.com/201dreamers/automation-framework/blob/main/docs/running_tests.md)
- [Working with Git](https://github.com/201dreamers/automation-framework/blob/main/docs/working_with_git.md)


#### Project structure
```
.
├── config
│   ├── device_secrets.py
│   ├── __init__.py
│   ├── loggers.py
│   └── paths.py
├── docs
│   ├── code_formatting.md
│   ├── reporting.md
│   ├── running_tests.md
│   └── working_with_git.md
├── pytest.ini
├── README.md
├── resources
│   ├── console_commands.yaml
│   ├── devices.yaml
│   ├── lib
│   └── testdata
├── src
│   ├── connectors
│   │   ├── base_connection.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   ├── serial_connection.py
│   │   └── ssh_connection.py
│   ├── device_lib
│   │   ├── device_lib.py
│   │   └── exceptions.py
│   └── devices
│       ├── device_parser.py
│       └── __init__.py
└── tests
    ├── conftest.py
    └── framework_checks
        └── smoke_test.py
```

The core functionality of the framework includes:

1. Ability to establish a connection with a testing device via SSH or Serial connection. This allows automated testing on devices while preserving configurations and settings. Additionally, it is possible to extend connection types if necessary, as the architecture used allows for this flexibility.
2. The framework enables storing the configuration of numerous testing devices, simplifying management and access to required settings for automated testing.
3. Provides intuitive abstractions for interacting with device console commands, facilitating easy and efficient testing using commands without needing an in-depth understanding of their internal implementation.
4. Allows easy creation of tests, focusing on their functionality and verification, without needing intricate details of connection and interaction with testing devices. This simplifies the test creation process and makes them more understandable and maintainable.
5. Supports the automatic generation of reports in the Allure format, providing a convenient way to visualize test results and quickly obtain and analyze data regarding test execution for easy interpretation and decision-making.

The primary goal of this framework is to simplify the process of automated testing and provide a convenient and reliable interface for interaction with testing devices.

#### Cloning the Repository using SSH:

To clone this repository, first, it is necessary to generate an SSH key and add it to your private GitHub account. Below are the sequential steps:

1. Open the terminal on your local machine and enter the command
   `ssh-keygen -t ed25519 -C "your_email@example.com"`
   where `your_email@example.com` is the email associated with your private GitHub account. During key generation, you'll be prompted to specify the location to save the key and a password to protect it.

2. Next, start the ssh agent in the background.
   `eval "$(ssh-agent -s)"`
   Depending on your environment, you might need to use a different command. For instance, use root access by running `sudo -s -H` before starting ssh-agent or use `exec ssh-agent bash` or `exec ssh-agent zsh` to start ssh-agent.

3. The next step is to add your private SSH key to the ssh-agent. If the key was created with a different name, replace `id_ed25519` in the command with the actual filename of your private key.
   `ssh-add ~/.ssh/id_ed25519`

These commands help create an ssh agent in the background and add the specified private key to the ssh agent for subsequent use during authorization. The generated key needs to be added to your GitHub account. To do this, log in to your private GitHub account. Click on your avatar in the upper right corner of the page, choose "Settings," then on the left side select "SSH and GPG keys," and click on "New SSH key" or "Add SSH key" (Fig. 3.1). Next, copy the contents of the `~/.ssh/id_rsa.pub` file on your local machine (this is the public SSH key) and paste it into the respective field on GitHub.

The final step is to clone the repository to your local machine. Using the command line, navigate to the directory where the cloned version of the repository will be stored and execute the command
`git clone git@github.com:201dreamers/automation-framework.git`

These steps ensure the successful creation of an SSH key, its addition to your GitHub account, and the cloning of the repository to your local machine, ensuring a secure and protected channel of communication between your data and the GitHub server.

### Storing Sensitive Data

In this project, sensitive data that should not be published in the repository is stored as environment variables. This approach assumes that every engineer working with the project independently sets these variables in their working environment. For example, sensitive data like the device username (`DEVICE_USERNAME`) and device password (`DEVICE_PASSWORD`) should be manually set.

To set environment variables, you can use your operating system's command line:

```bash
export DEVICE_USERNAME=your_username
export DEVICE_PASSWORD=your_password
```

This approach is secure and beneficial for several reasons:

- Storing sensitive data as environment variables avoids their publication in an open repository, reducing the risk of unauthorized access to this information.
- Each engineer can configure their working environment by setting their values for environment variables, enabling individual customization without the need to alter the project's shared code.
- This approach simplifies managing confidential data, as it doesn't require constant changes in the code or repository to modify sensitive information.

This approach of storing sensitive data as environment variables is essential for security and operational efficiency, as it helps prevent inadvertent disclosure of confidential information and streamlines the configuration of each engineer's working environment.

### Creating a Virtual Environment and Installing Dependencies

In this project, Python 3.11 is used. To ensure environment isolation and avoid dependency conflicts, it's recommended to create a virtual environment named `venv`.

To create the virtual environment, execute:

```bash
python3 -m venv venv
```

To activate the virtual environment, use the following commands depending on your operating system:

On Windows:
```bash
venv\Scripts\activate
```

On Unix or MacOS:
```bash
source venv/bin/activate
```

After activating the virtual environment, use the following command to install all necessary dependencies using pip, where the `requirements.txt` file contains all the project's necessary dependencies:

```bash
pip install -r requirements.txt
```

Libraries and modules that are dependencies of this project:

- `pyyaml`: Library for working with YAML files, enabling reading and writing data in YAML format.
- `paramiko`: Python SSH client that allows interaction with devices via the SSH protocol.
- `ipython`: Powerful interactive shell for Python providing enhanced development and experimentation capabilities.
- `pyserial`: Library for working with the Serial port in Python, facilitating interaction with devices through RS-232/RS-485 ports.
- `pytest-instafail`: Pytest plugin providing immediate test results display during execution.
- `pytest-timeout`: Pytest plugin allowing timeouts to be set for tests.
- `allure-pytest`: Plugin for collecting test results and generating reports in Allure format.
- `pytest-check`: Pytest plugin offering various checks during test execution.
- `loguru`: Simple and elegant logging library in Python, allowing convenient organization of logs in programs.
- `python-lsp-server`: Language Server Protocol (LSP) server to support editors and tools that support LSP for working with Python.
- `ruff`: Linter that checks code files for various types of errors and compliance with project standards.

Installing these libraries into the virtual environment ensures the necessary development, testing, and optimization capabilities of the project while maintaining version compatibility and security.
