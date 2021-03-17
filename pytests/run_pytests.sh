#!/bin/bash
set -eu

echo "[PYTEST] start run pytest."
cd ${HOME}/Workspaces/zj_py3_project/pytests 

# run specified test
pytest -v -s test_pytest.py --alluredir outputs/results/
# pytest -v -s test_pytest_fixtures.py --alluredir outputs/results/
# run all test
#pytest -v -s ./ --alluredir outputs/results/
# run test_base first to init env
# pytest -v -s ./test_pytest_base.py ./ --alluredir outputs/results/

echo "[PYTEST] generate allure report."
allure generate outputs/results/ -o outputs/reports/ --clean

echo "[PYTEST] pytest done."

set +eu