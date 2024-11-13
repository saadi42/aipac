import logging
import argparse
from flask import Flask, request, jsonify
from aipac.extract import Extractor
from config.logger import setup_logger

# Initialize the logger
setup_logger()
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run():
    """
    Endpoint to trigger FEC data extraction.

    Query Parameters:
        data_type (str): Specify which data type to extract ("receipts" or "disbursements").

    Returns:
        JSON response with a message indicating success or error.
    """
    data_type = request.json.get("data_type")

    if data_type not in ["receipts", "disbursements"]:
        logger.error("Invalid data_type specified. Choose 'receipts' or 'disbursements'.")
        return jsonify({"error": "Invalid data_type. Choose 'receipts' or 'disbursements'."}), 400

    logger.info(f"Starting {data_type} extraction")

    try:
        extractor = Extractor()
        extractor._extract_all(data_type)
        logger.info(f"{data_type.capitalize()} extraction completed successfully")
        return jsonify({"message": f"{data_type.capitalize()} extraction completed successfully"}), 200
    except Exception as e:
        logger.error(f"An error occurred during {data_type} extraction", exc_info=True)
        return jsonify({"error": "An error occurred during extraction", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
