## Step 1: Virtual environment 
    python -m venv .
    source ./bin/activate
    install Python 3.8.5

## Step 2: Install all the python dependencies
    pip install -r requirements.txt

## Setp 3: Run backend
    python server.py
    
##    Upload a json file with the plans of the Empire in the user interface. Submit query.

## For running the CLI:

    dist/give-me-the-odds millennium-falcon.json <path to empire.json>

    For example:
    dist/give-me-the-odds millennium-falcon.json examples/example1/empire.json

