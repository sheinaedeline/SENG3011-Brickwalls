# SENG3011-Brickwalls
Mentor: Yi Zhuang

This team consists of 5 members:
Z5205003 Allen Wu
Z5207915 Monica He
Z5207001 Vishnu Pillai
Z5228933 Kshitiz Saini
Z5190299 Sheina Edeline Tengara

## API

The API is hosted on Azure and can be found here: https://diseasereportapi.azurewebsites.net/

## Running API on local server

Run the virtual environment
```bash
source .venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

Run local server API
```bash
python3 application.py
```
## Running API test files

The test files are in: 
```bash
PHASE_1/Test_files
```
Test the articles endpoint
```bash
python3 articlesTest.py
```
Test the restrictions endpoint
```bash
python3 restrictionsTest.py
```

## Logs and Log file
There are two types of logs in the API. One returns a json snippet with the API response to the end user,
which includes the details such as team name, accessed time, time taken to address the request, status code and endpoint.
There is also a log file located at:
```bash
PHASE_1/API_SourceCode/Azure_Flask/log_file.txt
```
It contains details such as which API end point was accessed at what time, how long it took to address the request and the status code.

## API Documentation
The API documentation was done utilising Stoplight.io.
The JSON file with the API documentation is located:
```bash
PHASE_1/API_Documentation/Disease-Reports-API.v1.json
```
