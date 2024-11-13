from google.cloud import bigquery

class BigqueryClient:

    def __init__(self):
        self._client = bigquery.Client()

    def _insert_data(self, json_rows, dataset_id, table_id):
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
        return self._client.query_and_wait(query)
