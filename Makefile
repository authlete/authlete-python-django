#
# Copyright (C) 2019-2024 Authlete, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.


#==================================================
# VARIABLES
#==================================================
PYTHON = python3
TOOLS  = setuptools twine wheel


#==================================================
# TARGETS
#==================================================
.PHONY: _default clean clean-dist clean-python dist \
  help release test test-upload upgrade-tools


_default: help


clean: clean-dist clean-python


clean-dist:
	@rm -rf build dist *.egg-info


clean-python:
	@find . -name "__pycache__" -prune -exec rm -rf '{}' \;
	@find . -name "*.py[cdo]" -exec rm -rf '{}' \;


# Why you shouldn't invoke setup.py directly
#   https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
#
dist:
#	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) -m build --sdist --wheel


help:
	@printf '%s\n' \
	"clean         - removes generated files." \
	"clean-dist    - removes files generated for distribution." \
	"clean-python  - removes files generated by python." \
	"dist          - builds a distribution." \
	"help          - shows this help text." \
	"release       - releases a distribution to https://pypi.org/." \
	"test          - runs tests." \
	"test-upload   - uploads a distribution to https://test.pypi.org/." \
	"upgrade-tools - upgrades the following tools: $(TOOLS)"


release:
	$(PYTHON) -m twine upload dist/*


test:
	$(PYTHON) -m unittest discover


test-upload:
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upgrade-tools:
	$(PYTHON) -m pip install --user --upgrade $(TOOLS)
