from google.cloud import bigquery

class BigqueryClient:
    """
    A client for interacting with Google BigQuery, providing methods to insert JSON data 
    into a specified table and to execute SQL queries.

    This class uses the Google Cloud BigQuery client library to load data in JSON format 
    into BigQuery tables and to retrieve data using SQL queries.

    Attributes:
        _client (bigquery.Client): An instance of BigQuery Client for executing 
        BigQuery operations.
    """
    def __init__(self):
        """
        Initializes the BigqueryClient with an instance of the Google Cloud BigQuery client.

        This client instance (`self._client`) is used to execute data loading and querying operations.
        """
        self._client = bigquery.Client()

    def _insert_data(self, json_rows, dataset_id, table_id):
        """
        Inserts JSON rows into a specified BigQuery table.

        Args:
            json_rows (list): A list of dictionaries where each dictionary represents a row of data in JSON format.
            dataset_id (str): The ID of the BigQuery dataset.
            table_id (str): The ID of the BigQuery table within the specified dataset.

        Returns:
            google.cloud.bigquery.LoadJob: The completed BigQuery load job object, which includes information about the load operation.

        Raises:
            google.cloud.exceptions.GoogleCloudError: If the load job fails.
        """
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

        _dataset = self._client.dataset(dataset_id)
        _table = _dataset.table(table_id)

        job = self._client.load_table_from_json(
            json_rows=json_rows, 
            destination=_table,
            job_config=job_config
        )
    
        job.result()
        return job

    def _fetch_data(self, query):
        """
        Executes a SQL query and fetches results from BigQuery.

        Args:
            query (str): The SQL query to be executed in BigQuery.

        Returns:
            google.cloud.bigquery.table.RowIterator: An iterator over the rows of the query result.

        Raises:
            google.cloud.exceptions.GoogleCloudError: If the query job fails.
        """
        return self._client.query_and_wait(query)
