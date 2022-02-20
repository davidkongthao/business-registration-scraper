import requests
import json
import re
from bs4 import BeautifulSoup

class Search(object):

    class Minnesota(object):
        def __init__(self, url):
            self.url = url
    
        def construct_query_url(self, search_query):
            url = self.url.format(search_query)
            return url

        def parse_data(self, data):
            parsed_page = BeautifulSoup(data.text, "html.parser")
            return parsed_page

        def splice_data(self, data):
            spliced_data = data.split(", ")
            city = spliced_data[0]
            # Splice data down further to get the state, and postal code
            spliced_data = spliced_data[1].split(" ")
            state = spliced_data[0]
            postal_code = spliced_data[1]
            return [city, state, postal_code]

        def filter_parsed_data(self, data):
            filtered_businesses = data.find_all("tr")
            businesses = []
            for business in filtered_businesses:
                context = {}

                name = business.find("strong")
                if name != None:
                    """
                    This is to handle the name case execeptions because querying this site can sometimes throw a NoneType error.
                    """
                    context["business_name"] = name.get_text()

                extracted_url = business.find("a")
                if extracted_url != None:
                    """
                    This is meant to extract the URLs from the site, query the site, and get information regarding the company.
                    """
                    constructed_url = "https://mblsportal.sos.state.mn.us/{}".format(extracted_url.get("href"))
                    context["filing_url"] = constructed_url
                    business_query = requests.get(constructed_url)
                    if business_query.status_code == 200:
                        business_page = BeautifulSoup(business_query.text, "html.parser")
                        business_data = business_page.find("div", {"id": "filingSummary"})
                        data_items = business_data.find_all("dl")
                        for item in data_items:
                            header = item.find("dt").get_text()
                            value = item.find("dd").get_text()

                            # This is to format the address before pushing it off into the context.
                            if "Registered Office Address" in header or "Principal Executive Office Address" in header:
                                value = item.find("dd")
                                breaks = value.find_all("br")
                                num_breaks = len(breaks)
                                
                                for br in value.find_all("br"):
                                    br.replace_with("split")
                            
                                address_data = value.get_text().split("split")
                                address = {}
                                if num_breaks == 2:
                                    if "#" in address_data[0]:
                                        split_data = address_data[0].split("#")
                                        address["line1"] = split_data[0]
                                        address["line2"] = "#{}".format(split_data[1])             
                                    else:
                                        address["line1"] = address_data[0]
                                        address["line2"] = None
                                    
                                    data = self.splice_data(address_data[1])
                                    address["city"] = data[0]
                                    address["state"] = data[1]
                                    address["postal_code"] = data[2]
                                    
                                
                                if num_breaks == 3:
                                    address["line1"] = address_data[0]
                                    address["line2"] = address_data[1]

                                    data = self.splice_data(address_data[2])
                                    address["city"] = data[0]
                                    address["state"] = data[1]
                                    address["postal_code"] = data[2]
                                
                                address["country"] = "USA"
                                
                                value = address

                            match header:
                                case "Filing Date": context["filing_date"] = value
                                case "Registered Office Address": context["registered_office_address"] = value
                                case header if "Officer" in header or "Manager" in header: context["officer"] = value
                                case "Status": context["status"] = value
                                case "Principal Executive Office Address": context["principal_address"] = value
                            
                            context["state"] = "Minnesota"

                businesses.append(context)
            return businesses

        def query_response(self, search_query):
            url = self.construct_query_url(search_query)
            response = requests.get(url)
            parsed_page = self.parse_data(response)
            filtered_data = self.filter_parsed_data(parsed_page)
            return filtered_data
