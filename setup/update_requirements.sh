#!/bin/bash

# Exit the script if any command fails
set -e

# Define the filenames
CURRENT_PACKAGES_FILE="current_packages.txt"
SYSTEM_PACKAGES_FILE="system_packages.txt"
UPDATED_REQUIREMENTS_FILE="requirements.txt"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment is not activated."
    echo "Please activate your virtual environment and try again."
    exit 1
fi

# Generate the list of installed packages in the virtual environment
pip freeze > "$CURRENT_PACKAGES_FILE"

# Generate the list of globally installed packages
# Note: We use a trick here by creating a temporary virtual environment with system packages
# for comparison, since `pip freeze --system-site-packages` might not work as expected.
TEMP_VENV=$(mktemp -d)
python -m venv "$TEMP_VENV" --system-site-packages
source "$TEMP_VENV/bin/activate"
pip freeze > "$SYSTEM_PACKAGES_FILE"
deactivate
rm -rf "$TEMP_VENV"

# Compare and filter out system packages
comm -23 <(sort "$CURRENT_PACKAGES_FILE") <(sort "$SYSTEM_PACKAGES_FILE") > "$UPDATED_REQUIREMENTS_FILE"

# Clean up temporary files
rm "$CURRENT_PACKAGES_FILE" "$SYSTEM_PACKAGES_FILE"

echo "Updated requirements have been written to $UPDATED_REQUIREMENTS_FILE"
