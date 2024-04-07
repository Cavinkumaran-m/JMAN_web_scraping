import requests
import json
import pandas
from alive_progress import alive_bar


print("\nWeb Scraper for the Lenskart Site\n")

try:
    # Logic to read api endpoints from the file
    with open("api_endpoints.txt", "r") as APIs:
        apis = []
        while(True):
            api = APIs.readline()
            if len(api) == 0:
                break
            elif api[0] == "#":
                apis.append({"status":api[1:].replace("\n","")})
            else:
                api = api.replace("\n","")
                apis.append(api)

        # Logic for data parsing along with the progress bar
        with alive_bar(len(apis), dual_line=True, bar="smooth") as bar:
            products = []
            for api in apis:
                bar()
                if type(api) is dict:
                    bar.text = "->\tFetching: "+api["status"]
                else:
                    json_data = requests.get(api).json()
                    products.extend(json_data["result"]["product_list"])
                data = pandas.DataFrame(products)
                data.to_csv("output.csv", encoding="utf-8", index=False)


except Exception as Ex:
    print("The following error has occurred:\n ", Ex)