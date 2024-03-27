

## Development env setup (27/03/2024)


### 1. Create Py VENV
```
- python3.10 -m venv venv

    python -V
    Python 3.10.12

python3.10 -m venv venv; source venv/bin/activate; pip install -r polishness/requirements.txt
```


### 2. Install Py packages
```
- pip install -r polishness/requirements.txt

    pip list
    Package         Version
    --------------- -----------
    attrs           23.2.0
    click           8.1.3
    exceptiongroup  1.2.0
    Flask           2.2.2
    iniconfig       2.0.0
    itsdangerous    2.1.2
    Jinja2          3.1.3
    MarkupSafe      2.1.5
    marshmallow     3.19.0
    numpy           1.26.4
    packaging       24.0
    pandas          1.5.3
    pip             22.0.2
    pluggy          1.4.0
    pytest          7.2.2
    python-dateutil 2.9.0.post0
    pytz            2024.1
    setuptools      59.6.0
    six             1.16.0
    tomli           2.0.1
    Werkzeug        2.2.2
```


### 1 + 2
```
python3.10 -m venv venv; source venv/bin/activate; pip install -r polishness/requirements.txt
```


### 3. setup DB
```
- PYTHONPATH=. python polishness/api/monuments/monuments_tools.py
- Pycharm: run 'db_setup' configuration   
```


### 4. Start APP
```
- Run app: PYTHONPATH=. python polishness/app.py
- Pycharm: run 'app' configuration
```


### 3+4
```
- Pycharm: run 'run_all_from_scratch'
```


### 1 + 2 + 3 + 4 (terminal - like)
```
python3.9 -m venv venv; source venv/bin/activate; pip install -r polishness/requirements.txt; PYTHONPATH=. python polishness/api/monuments/monuments_tools.py; PYTHONPATH=. python polishness/app.py
```
