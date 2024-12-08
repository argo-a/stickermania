#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install test dependencies
pip install -r ../requirements.txt

# Add backend directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests with coverage
pytest \
    --verbose \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html:coverage_report \
    tests/

# Open coverage report if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open coverage_report/index.html
fi

# Print test summary
echo "Test Summary:"
echo "============"
coverage report
