#!/bin/bash

tag="[PYTEST]"

if [[ $1 == "mail" ]]; then
    echo "$tag send email with archived test results."
    cd ${PYPATH}/apitest && python3 common/email_helper.py
    exit $? 
fi

echo "$tag clear old test run logs."
cd ${PYPATH}/apitest && rm outputs/logs/*.txt

if [[ -z $1 ]]; then
    echo "$tag start run api test."
    # run test_base.py first to init env and load data
    pytest -v -s testcases/test_base.py testcases/ --html=outputs/api-report.html
    # pytest cli log options
    #-vv -o log_cli=true -o log_cli_level=INFO --log-date-format="%Y-%m-%d %H:%M:%S" 
    #--log-format="%(filename)s:%(lineno)s %(asctime)s %(levelname)s %(message)s"
elif [[ $1 == "report" ]]; then
    echo "$tag start run api test."
    pytest -v -s testcases/test_base.py testcases/ --alluredir outputs/results/
    echo "$tag generate allure report."
    allure generate outputs/results/ -o outputs/reports/ --clean
    # outputs: logs/ results/ reports/
else
    echo "invalid input args!"
    exit 99
fi

echo "$tag api test done."
