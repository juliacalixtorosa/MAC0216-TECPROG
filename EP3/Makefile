.PHONY: doc tests clean

DOC_DIR = docs
SRC_DIR = src
TEST_DIR = test
PYTHON = python3
VENV_DIR = venv

all: doc tests

doc:
	doxygen Doxyfile

tests:
	cd $(TEST_DIR) && $(PYTHON) -m pytest -v

clean:
	rm -rf $(DOC_DIR)
	rm -rf $(TEST_DIR)/__pycache__
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf .pytest_cache
	rm -rf $(VENV_DIR)
