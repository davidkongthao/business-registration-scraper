import os
import json
from search import Search

MINNESOTA_URL = "https://mblsportal.sos.state.mn.us/Business/BusinessSearch?BusinessName={}&IncludePriorNames=False&Status=Active&Type=BeginsWith"

def main():
    search_module = Search.Minnesota(url=MINNESOTA_URL)
    search_query = "AAA"
    data = search_module.query_response(search_query)
    if data is not None:
        for item in data:
            print(f"\n {item} \n")

if __name__ == "__main__":
    main()