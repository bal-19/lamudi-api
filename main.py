from scrape.lamudi import Lamudi
from urllib.parse import quote_plus
from fastapi import FastAPI
from enum import Enum

class Filter(str, Enum):
    buy = "buy"
    rent = "rent"

app = FastAPI()

@app.get("/lamudi/")
def get_data_kios(filter: Filter, keyword: str, total_pages: int = 1):
    """
    <h3>INPUT EXAMPLE:</h3>
    <p>keyword: jakarta, jakarta selatan, apartemen</p>
    <p>total_pages: 1, 2, 3, 10 (note: untuk maksimal total halaman 50)</p>
    """
    url = f"https://www.lamudi.co.id/{filter.value}/?q={quote_plus(keyword)}&page=1"
    
    result = Lamudi(url=url, fillter=filter, keyword=keyword, total_pages=total_pages).get_data()
    return result