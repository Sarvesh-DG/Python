# python-unittest-exercise



## Getting started

Install `virtualenv` using `pip`
```bash
pip install virtualenv
```

Create the `virtualenv` for this project
```bash
virtualenv venv
#------OR------#
python -m virtualenv venv
```

Activate `virtualenv` 
- (For windows):
    ```bash
    # Enable powrshell script execution by opening Powershell as Administrator and then use the command below:
    Set-ExecutionPolicy RemoteSigned

    # Then activate the virtualenv
    ./venv/Scripts/activate
    ```
- (For Linux):
    ```bash
    . venv/bin/activate
    ```


Install the dependencies required for run tests
```bash
pip install -r requirements.txt
```

Run the unit tests
```bash
pytest
#------OR------#
python -m pytest
```


## Goal:
- First read about these topics:
    - Unit testing and why it is required: 
        - https://smartbear.com/learn/automated-testing/what-is-unit-testing/#:~:text=A%20unit%20test%20is%20a,of%20the%20definition%20is%20important.
        - https://fortegrp.com/the-importance-of-unit-testing/
    - Unit testing vs Integration testing vs Functional testing:
        - https://www.softwaretestinghelp.com/the-difference-between-unit-integration-and-functional-testing/
    - Test driven development:
        - https://www.guru99.com/test-driven-development.html
    - Mocking & Stubbing in unit testing:
        - https://circleci.com/blog/how-to-test-software-part-i-mocking-stubbing-and-contract-testing/
- Fork the project.
- Clone the repo.
- Create a child(feature) branch from master/main branch.
- In the child(feature) branch, implement the changes mentioned below

    1. Tests are already written for functins present in [tdd_example.py](src/tdd_example.py) in [test_tdd_example.py](tests/test_tdd_example.py).Complete the implementation of all 4 methods in [tdd_example.py](src/tdd_example.py) for making the tests Pass.
    1. Implement the unit test cases for the methods in `general_example.py`
        - You can use `unittest` or `pytest` for implementing test cases.
        - `Note`: Mock the [load_employee_rec_from_database()](src/general_example.py#L16) method while writing unit test for [fetch_emp_details()](src/general_example.py#L22) method.
    2. Complete the implementation of 3 test methods in [test_dynamodb_example.py](tests/test_dynamodb_example.py). Take a referece from the [test_s3_example.py](tests/test_s3_example.py)
        - `moto` is the package being used for mocking boto3 api calls: http://docs.getmoto.org/en/latest/docs/getting_started.html
    3. Run the test cases. All test cases should pass.
    4. Generate the code coverage report.
        - More about code coverage:
            - https://www.atlassian.com/continuous-delivery/software-testing/code-coverage
            - https://www.sealights.io/agile-testing/test-metrics/python-code-coverage/
- Push the child(feature) branch from local to the remote.

## Deliverables:
- Share the link to your repo.

