## Running Tests and pytest Options

Within the pytest framework, there are several diverse options providing capabilities to manage and configure the test execution process. Below are the most commonly used options during daily runs:

- **-m:** Option for selecting tests by marker. It allows executing only those tests that have the specified marker. For example: `-m smoke` will execute tests marked as "smoke".

- **-k:** Filters tests based on a string in their names. For instance: `-k test_login` will execute only tests whose name contains "test_login".

- **--connection, --device:** Options to specify device connection parameters or its identifier. These can be used in tests requiring a specific device for execution.

- **--alluredir, --clean-alluredir:** Options to specify the directory where Allure report files will be saved and to clean that directory before test execution.

- **-x, --maxfail:** Options to stop test execution after a certain number of test failures (`-x` stops after the first failure, while `-maxfail=N` stops after N failed tests).

- **--pdb, --pdbcls:** Options to enable Python's debugger (pdb) in case of test failures (`--pdb` sets the debugger by default, and `--pdbcls` allows selecting an alternative debugger).

These options provide engineers with greater flexibility and control while executing tests using pytest. Each option serves a specific purpose, allowing customization of test execution according to testing requirements, contributing to improving the efficiency of the testing process and the speed of error detection.
