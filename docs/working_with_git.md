### Repository Workflow Rules

The branch name should always start with the task number. This allows tracking changes in the tracking system. To create a branch, execute the following commands in the root folder of the repository:

```bash
git checkout -b <TICKET-XXX_NEW_BRANCH_NAME>
```

The NEW_BRANCH_NAME could be a brief ticket description to facilitate branch search. Allowed characters for branch name: underscores, dashes, slashes, and alphanumeric characters. For example: PROJ-123_fix_connection_issue

Before committing changes, it's essential to stage the files. To preview the changes that can be committed, use git status. The list of files will be listed under the header "Changes not staged for commit."

To add files to commit, you can use:

```bash
git add <FILENAME>
git add -u
```

After staging files for commit, execute the command, mentioning the task number in the message, allowing to track commits related to the ticket:

```bash
git commit -m "TICKET-XXX <COMMIT MESSAGE>"
```

To send changes to the remote repository and set up tracking, execute the following on your local branch:

```bash
git push --set-upstream origin HEAD
```

This will send your local branch to the remote repository and set up tracking for it. With tracking, when executing git status, you can see the state of the local branch compared to the remote branch. For instance, the number of local commits that haven't been pushed yet.

Once the branch is set to track the remote one, for all future cases, use git push.

### Creating a Pull Request (PR)

To create a PR on GitHub, navigate to the Pull requests tab and click on New pull request in the upper right corner. Then, select the base branch and choose the target branch (usually master or main). It will display the differences, showcasing modified files and commits. Click Create pull request and add relevant reviewers to the merge request, selecting the cog icon in the right sidebar.

In the description of this request, it's essential to fill in the following template, allowing all reviewers to quickly understand the purpose of this pull request and the changes present in it. This reduces the time spent on review and helps conserve team resources.

#### PR template:
<!-- Update ticket number, hyperlink will automatically form -->
PROJ-XXX

**KPI Metrics**
| Metric                 | Count |
|------------------------|-------|
| Test Cases Modified    | 0     |
| Test Cases Added       | 6     |
| Library Improvements   | 0     |
| Framework Improvements | 1     |

<!-- Please provide of a one line summary of each library improvement  -->
**Library Improvements**
* N/A

<!-- Please provide of a one line summary of each framework improvement  -->
**Framework Improvements**
* N/A

<!-- Please provide of a one line summary of each test case type added  -->
**Test Case Summary**
* N/A

---
**Description**
<!-- Please describe the changes in this PR -->

---
**Run Command**
```bash
pytest ...
```

---
**Screenshot of Passing Result**
