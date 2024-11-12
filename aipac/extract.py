import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List
from aipac.gcp_client import BigqueryClient

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Extractor:

    def __init__(self):
        self.api_call_count = 0
        self.BASE_URL = "https://api.open.fec.gov/v1/"
        self.API_CALL_LIMIT = 1000

        self.bq_client = BigqueryClient()

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
        if self.api_call_count >= self.API_CALL_LIMIT:
            raise Exception("API Call limit reached, try again in an hour.")
        
        try:
            response = requests.get(
                url=f"{self.BASE_URL}/{endpoint}",
                params=params
            )
            # Raise an exception for HTTP error responses
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

        return self.bq_client._insert_data(json_rows, dataset_id, table_id)
        
    def _get_last_indexes(
        self,
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
