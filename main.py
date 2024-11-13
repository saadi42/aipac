import logging
from typing import Dict, Any, List
from aipac.extract import Extractor
from aipac.constants import ConstantsManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def _update_api_params(src: Dict[str, Any], params: Dict[str, Any], keys: List):
    for _ in keys:
        params[_] = src[_]
    
def main():
    """Fetch data from FEC API
    """

    extractor = Extractor()
    ct = ConstantsManager()

    logger.info(f"starting {ct.AIPAC_BQ_DATASET} extraction for {ct.RECEIPTS_BQ_TABLE} endpoint")

    # NOTE: Donot change these values until all data is extracted.
    # The checkpoint helps continue extraction from the last index, provided params stay same.
    params = {
        "api_key": ct.API_KEY,
        "committee_id": [ct.AIPAC_COMMITTEE_ID],
        "sort": f"{ct.RECEIPTS_LAST_DATE}",
        # "per_page": ct.API_MAX_RESULTS_PER_PAGE,
        "per_page": 2,
        "min_date": "2023-10-07",
        "max_date": "2023-10-07",
        "min_amount": 50,
        "max_amount": 50
    }

    checkpoint = extractor._get_last_indexes(ct.AIPAC_BQ_DATASET, ct.RECEIPTS_BQ_TABLE, ct.RECEIPTS_LAST_DATE)
    if checkpoint:
        logger.info(f"getting last_index from bigquery table {ct.RECEIPTS_BQ_TABLE} as \n: {checkpoint}")
        params["last_index"] = checkpoint["last_index"]
        params["last_contribution_receipt_date"] = checkpoint["last_contribution_receipt_date"]
    
    while True:
        response = extractor._get_schedule_response(endpoint=ct.RECEIPTS_ENDPOINT, params=params)

        if (extractor.api_call_count == 1):
            logger.info(f"""Total results: {response["pagination"]["count"]}""")
            logger.info(f"""Total pages: {response["pagination"]["pages"]}""")

        if len(response["results"]) != 0:
            job = extractor._upload_schedule_response(response, ct.AIPAC_BQ_DATASET, ct.RECEIPTS_BQ_TABLE)
            logger.info(f"Loaded {job.output_rows} rows into {ct.AIPAC_BQ_DATASET}:{ct.RECEIPTS_BQ_TABLE}. Api call count: {extractor.api_call_count}")

        last_indexes = response["pagination"]["last_indexes"]
        if last_indexes is None:
            logger.info("Exiting. Last_indexes is empty in pagination.")
            break
        
        params["last_index"] = last_indexes["last_index"]
        params["last_contribution_receipt_date"] = last_indexes["last_contribution_receipt_date"]
    
    logger.info(f"Total api calls made: {extractor.api_call_count}")

if __name__ == "__main__":
    main()
