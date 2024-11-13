import logging
from aipac.extract import Extractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    extractor = Extractor()

    extractor._extract_all("receipts")
    extractor._extract_all("disbursements")

if __name__ == "__main__":
    main()
