if [ ! -e venv ]
then
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
pip install --editable .

while true; do
    a-gis
    if [ $? -eq 0 ]; then
        echo "Script ran successfully!"
        break
    fi
    missing_package=$(a-gis 2>&1 | grep "ModuleNotFoundError" | awk -F"'" '{print $2}')
    if [ -n "$missing_package" ]; then
        echo "Installing missing package: $missing_package"
        pip install "$missing_package"
    else
        echo "No missing package detected, exiting..."
        break
    fi
done

echo running tests

pytest -n 6 .

