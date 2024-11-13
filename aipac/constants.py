import os
from typing import Any


class Constants:
  API_KEY = os.environ["FEC_API_KEY"]
  BASE_URL = "https://api.open.fec.gov/v1/"
  API_CALL_LIMIT = 1000
  API_MAX_RESULTS_PER_PAGE = 100
  AIPAC_COMMITTEE_ID = "C00797670"
  AIPAC_BQ_DATASET = "aipac"
  RECEIPTS_ENDPOINT = "schedules/schedule_a"
  RECEIPTS_BQ_TABLE = "temp"
  RECEIPTS_LAST_DATE = "contribution_receipt_date"


class ConstantsManager:
  def __init__(self):
    for cls in [Constants]:
      for key, value in cls.__dict__.items():
        if not key.startswith("__"):
          self.__dict__.update(**{key: value})

    
  def __setattr__(self, name: str, value: Any) -> None:
    raise TypeError("Constants are immutable")
