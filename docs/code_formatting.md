### Code Formatting Rules

#### PEP8

Adhering to PEP 8 standards (Python's code style guide) is mandatory. PEP 8 is an official document containing recommendations for Python code style. It defines formatting rules, spacing, variable naming, comments, and other conventions that help create readable and consistent code in projects.

The guidelines include:

1. Use 4 spaces for indentation (avoid tabs).
2. Ensure consistent indentation throughout the project.
3. Recommended maximum line length for this project is 120 characters.
4. Keep comments and docstrings within 80 characters.
5. Avoid unnecessary whitespace at the start/end of lines or after commas, semicolons, etc.
6. Import each module separately.
7. Avoid using import *.
8. Use descriptive and meaningful names for variables, functions, methods, and classes.
9. Follow snake_case for functions/variables and PascalCase for classes.
10. Use clear comments to explain complex code segments.
11. Add docstrings for modules, classes, and functions.
12. Separate functions and classes with blank lines for readability.
13. Avoid generic exception handling like except Exception:. Choose specific exception types.
14. Align expressions for readability, but do not overdo alignment.
15. Use parentheses to break long logical lines of code.
16. Readability and Documentation:
17. Code should be understandable for other team members, prioritize code clarity over brevity.
18. Include comments and documentation for functions, especially if their purpose is not obvious.

#### pytest

1. Write clean and well-organized test code.
2. Use the pytest-check plugin to verify test result expectations if a test has more than two checks.
3. Provide understandable names for the tests they verify. Each test suite's name should start or end with test_ or _test, respectively.

#### Functions and Modules

1. Functions should perform a single specific task. Adhere to the Single Responsibility Principle.
2. Modules should be logically organized and contain related functionality.
3. Use exceptions for error handling instead of recovery with try-except.
4. General Practices:
5. Use modularity and code reuse, avoid code duplication.
6. Use Git for version control. Code should be stored and documented in the version control system.

#### Testing

1. Ensure all tests complete successfully before merging into the main branch.
2. Ensure all tests are working and cover necessary scenarios.
3. Teamwide conventions:
4. Define team-wide coding conventions and adhere to them.
5. Conduct regular code reviews and discussions to improve code quality.

These recommendations will ensure clean, organized, and easily understandable code for project automation engineers using Python and pytest.
