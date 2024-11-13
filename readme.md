## DESCRIPTION

This project fetches AIPAC receipts and disbursements data using [FEC API](https://api.open.fec.gov/developers/#/) and pushes to Bigquery.

# PRE-REQUISITES

* set env variable `FEC_API_KEY` by signing up on [FEC API site](https://api.open.fec.gov/developers/#/).

* Ensure gcloud authentication is setup.

* Ensure Bigquery datasets and tables are created. The schema for both schedule_a(receipts) and schedule_b(disbursements) is same as below.
```
[
  {
    "name": "created_at",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "results",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  }
]
```

# HOW DOES IT WORK

In terminal start the app
```
poetry run python3 app.py
```
In another terminal, run the following curl command
```
curl -X POST http://0.0.0.0:5000/run -H "Content-Type: application/json" -d '{"data_type": "receipts"}'
```

