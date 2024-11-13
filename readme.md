## DESCRIPTION

This project fetches AIPAC receipts and disbursements data using [FEC API](https://api.open.fec.gov/developers/#/) and pushes to Bigquery.

# PRE-REQUISITES

* set env variable `FEC_API_KEY` by signing up on [FEC API site](https://api.open.fec.gov/developers/#/)

* Ensure your

# HOW DOES IT WORK

In terminal start the app
```
poetry run python3 app.py
```
In another terminal, run the following curl command
```
curl -X POST http://0.0.0.0:5000/run -H "Content-Type: application/json" -d '{"data_type": "receipts"}'
```

