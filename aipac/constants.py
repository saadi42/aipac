import os

class Constants:
  """
  Constants class for holding static configuration values used in the application.

  This class centralizes important constant values required for API calls, dataset
  identifiers, and BigQuery table configurations, ensuring consistency and ease of 
  configuration changes.

  Attributes:
      API_KEY (str): The API key used to authenticate requests to the FEC API, obtained from environment variables.
      BASE_URL (str): The base URL for the FEC API endpoints.
      API_CALL_LIMIT (int): Maximum allowed API calls within a specified period.
      API_MAX_RESULTS_PER_PAGE (int): Maximum number of results per page for API requests.
      AIPAC_COMMITTEE_ID (str): The specific committee ID to filter data related to AIPAC.
      AIPAC_BQ_DATASET (str): BigQuery dataset name for storing the AIPAC data.
      
      DATA_CONFIG (dict): Dictionary of configurations for different data types such as "receipts" and "disbursements".

          Each data type configuration includes:
          - endpoint (str): API endpoint path specific to the data type.
          - bq_table (str): BigQuery table name where data will be stored.
          - last_date (str): Name of the date field to use for tracking data updates.
          - last_indexes (List[str]): List of field names used as checkpoint indexes for data continuity.

  Example:
      Usage of `Constants` class:
      
      ```python
      from constants import Constants
      endpoint = Constants.DATA_CONFIG["receipts"]["endpoint"]
      ```
  """
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
          "bq_table": "schedule_a",
          "last_date": "contribution_receipt_date",
          "last_indexes": ["last_index", "last_contribution_receipt_date"]
      },
      "disbursements": {
          "endpoint": "schedules/schedule_b",
          "bq_table": "schedule_b",
          "last_date": "disbursement_date",
          "last_indexes": ["last_index", "last_disbursement_date"]
      }
  }
