import os


class Constants:
  API_KEY = os.environ["FEC_API_KEY"]
  BASE_URL = "https://api.open.fec.gov/v1/"
  API_CALL_LIMIT = 1000
  API_MAX_RESULTS_PER_PAGE = 100
  AIPAC_COMMITTEE_ID = "C00797670"
  AIPAC_BQ_DATASET = "aipac"
  
  # Nested dictionaries for each data type
  DATA_CONFIG = {
      "receipts": {
          "endpoint": "schedules/schedule_a",
          "bq_table": "temp_a",
          "last_date": "contribution_receipt_date",
          "last_indexes": ["last_index", "last_contribution_receipt_date"]
      },
      "disbursements": {
          "endpoint": "schedules/schedule_b",
          "bq_table": "temp_b",
          "last_date": "disbursement_date",
          "last_indexes": ["last_index", "last_disbursement_date"]
      }
  }
