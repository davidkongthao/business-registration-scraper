from search import Search

MINNESOTA_URL = "https://mblsportal.sos.state.mn.us/Business/BusinessSearch?BusinessName={}&IncludePriorNames=False&Status=Active&Type=BeginsWith"

def main():
    search_module = Search.Minnesota(url=MINNESOTA_URL)
    results = []
    search_queries = [
        "AAAA", "AAA", "AA", "A",
        "AB", "ABB", "ABBB", "AC",
        "ACC", "ACCC"
    ]
    for query in search_queries:
        data = search_module.query(search_query=query)
        if data is not None:
            results += data

#    results = list(map(dict, set(tuple(sorted(sub.items())) for sub in results)))

    if results is not None:
        for item in results:
            print(f"\n {item} \n")
        
        print(f'Found a total of {len(results)} companies')

if __name__ == "__main__":
    main()