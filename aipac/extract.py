import json
import logging
import requests
from typing import Any, Dict, List
from datetime import datetime, timezone

from aipac.gcp_client import BigqueryClient
from aipac.constants import Constants

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Extractor:

    def __init__(self):
        self.bq_client = BigqueryClient()
        self.ct = Constants()

        self.api_call_count = 0
        self.rows_loaded = 0

    def _get_schedule_response(
        self,
        endpoint: str, 
        params: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Fetch a single page of results from the FEC API.

        Args:
            endpoint (str): API endpoint for Schedule A or B.
            params (ScheduleAParameters | ScheduleBParameters): Parameters to send with the API request.
        Returns:
           List[Dict[Any, Any]]: Parsed response schema containing results and pagination info.

        Raises:
            requests.HTTPError: If the request fails or the response status is not 200.
        """
        if self.api_call_count >= self.ct.API_CALL_LIMIT:
            raise Exception("API Call limit reached, try again in an hour.")
        
        try:
            response = requests.get(
                url=f"{self.ct.BASE_URL}/{endpoint}",
                params=params
            )
            response.raise_for_status()
            self.api_call_count += 1

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to fetch data from FEC API: {e}")
            raise

    def _upload_schedule_response(
        self,
        response: Dict[str, str],
        dataset_id: str,
        table_id: str
    ) -> None:
        """
        """
        _now = datetime.now(timezone.utc)

        resp_results = response["results"]

        json_rows = [
            {
                "results": json.dumps(nl),
                "created_at": str(_now)
            } 
            for nl in resp_results]

        job = self.bq_client._insert_data(json_rows, dataset_id, table_id)
        self.rows_loaded += job.output_rows
        return job

    def _get_last_indexes(self, 
        dataset_id: str,
        table_id: str,
        last_date: str
    ) -> Dict[str, Any]:
        # This table is manually created in Bigquery
        # The query should return one row
        query = f"""
            select
                json_value(results, "$.sub_id") as last_index,
                json_value(results, "$.{last_date}") as last_{last_date}
            from {dataset_id}.{table_id}
            qualify (row_number() over (order by last_index desc)) = 1
        """
        result = self.bq_client._fetch_data(query)
        rows = list(result)

        if rows:
            return [dict(row) for row in rows][0]

    def _update_api_params(self, src: Dict[str, Any], params: Dict[str, Any], keys: List) -> None:
        for _ in keys:
            params[_] = src[_]

    def _extract_all(self, data_type: str) -> None:
        """Fetch data from FEC API
        """
        bq_dataset = self.ct.AIPAC_BQ_DATASET
        try:
            config = self.ct.DATA_CONFIG[data_type]
            endpoint = config["endpoint"]
            bq_table = config["bq_table"]
            last_date = config["last_date"]
            last_indexes = config["last_indexes"]

        except KeyError:
            raise ValueError(f"Invalid data_type '{data_type}'. Choose either 'receipts' or 'disbursements'.")


        logger.info(f"Starting {bq_dataset} extraction for {data_type} endpoint")

        # NOTE: Donot change these values until all data is extracted.
        # The checkpoint helps continue extraction from the last index, provided params stay same.
        params = {
            "api_key": self.ct.API_KEY,
            "committee_id": [self.ct.AIPAC_COMMITTEE_ID],
            "sort": f"{last_date}",
            # "per_page": self.ct.API_MAX_RESULTS_PER_PAGE,
            "per_page": 5,
            "min_date": "2024-08-29",
            "max_date": "2024-08-29",
            "min_amount": 5000,
            "max_amount": 5000
        }
        logger.info(params)
        checkpoint = self._get_last_indexes(bq_dataset, bq_table, last_date)
        if checkpoint:
            logger.info(f"getting last_index from bigquery table {bq_table} as \n: {checkpoint}")
            self._update_api_params(checkpoint, params, last_indexes)
        
        while True:
            response = self._get_schedule_response(endpoint=endpoint, params=params)
            _pgn = response["pagination"]
            _rslt = response["results"]

            if (self.api_call_count == 1):
                logger.info(f"""Total results: {_pgn["count"]} \n Total pages: {_pgn["pages"]}""")

            if len(_rslt) != 0:
                job = self._upload_schedule_response(response, bq_dataset, bq_table)
                logger.info(f"Loaded {job.output_rows} rows into {bq_dataset}:{bq_table}. Api call count: {self.api_call_count}")

            res_last_indexes = _pgn["last_indexes"]
            if res_last_indexes is None:
                logger.info("Exiting. Last_indexes is empty in response")
                break
            
            self._update_api_params(res_last_indexes, params, last_indexes)
        
        logger.info(f"Total api calls made: {self.api_call_count}. Total row loaded: {self.rows_loaded}")
