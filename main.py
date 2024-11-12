import logging
import os
from aipac.extract import Extractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    """Fetch data from FEC API
    """

    extractor = Extractor()

    AIPAC_COMMITTEE_ID = 'C00797670'
    AIPAC_DATASET = "aipac"
    SCHEDULE_A_TABLE = "schedule_a"
    LAST_DATE = "contribution_receipt_date"
    MAX_RESULTS_PER_PAGE = 100

    logger.info(f"starting {AIPAC_DATASET} extraction for {SCHEDULE_A_TABLE} endpoint")


    enpoint = "schedules/schedule_a"
    params = {
        "api_key": os.environ["FEC_API_KEY"],
        "committee_id": [AIPAC_COMMITTEE_ID],
        "sort": f"{LAST_DATE}",
        "per_page": MAX_RESULTS_PER_PAGE,
        "min_date":"2023-10-01",
        "max_date":"2023-11-01"
    }

    checkpoint = extractor._get_last_indexes(AIPAC_DATASET, SCHEDULE_A_TABLE, LAST_DATE)
    if checkpoint:
        logger.info(f"getting last_index from bigquery table {SCHEDULE_A_TABLE} as \n: {checkpoint}")
        params["last_index"] = checkpoint["last_index"]
        params["last_contribution_receipt_date"] = checkpoint["last_contribution_receipt_date"]
    
    while True:
        response = extractor._get_schedule_response(endpoint=enpoint, params=params)

        if (extractor.api_call_count == 1):
            logger.info(f"""Total results: {response["pagination"]["count"]}""")
            logger.info(f"""Total pages: {response["pagination"]["pages"]}""")

        if len(response["results"]) != 0:
            extractor._upload_schedule_response(response, AIPAC_DATASET, SCHEDULE_A_TABLE)
            
        last_indexes = response["pagination"]["last_indexes"]
        if last_indexes is None:
            logger.info("Exiting since last_indexes is empty in pagination.")
            break
        
        params["last_index"] = last_indexes["last_index"]
        params["last_contribution_receipt_date"] = last_indexes["last_contribution_receipt_date"]
    
    logger.info(f"Total api calls made: {extractor.api_call_count}")
if __name__ == "__main__":
    main()
