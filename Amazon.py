import requests
from requests_html import HTMLSession
import pandas as pd

df = pd.read_csv("Url_file.csv")
roots = df["root"].tolist()


#roots = ["https://www.amazon.in/Redmi-10-Prime-extendable-Adaptive/dp/B09CTYGJSD/ref=sr_1_1?keywords=redmi&qid=1638602307&sr=8-1&th=1","https://www.amazon.in/Redmi-Activ-Carbon-Black-Storage/dp/B09GFPVD9Y/ref=sr_1_1?pf_rd_i=1389401031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=124f0688-89af-45c9-8e5a-04f4fbaecf32&pf_rd_r=AZV4R381SR42K23B0A3K&pf_rd_s=merchandised-search-19&pf_rd_t=101&qid=1638714239&refinements=p_36%3A1318505031%2Cp_85%3A10440599031&rps=1&s=electronics&sr=1-1","https://www.amazon.in/Tecno-Spark-Storage-Battery-Camera/dp/B096LS7N6Z/ref=sr_1_2?pf_rd_i=1389401031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=124f0688-89af-45c9-8e5a-04f4fbaecf32&pf_rd_r=AZV4R381SR42K23B0A3K&pf_rd_s=merchandised-search-19&pf_rd_t=101&qid=1638714239&refinements=p_36%3A1318505031%2Cp_85%3A10440599031&rps=1&s=electronics&sr=1-2"]

def getprice(url):
    proxy_list = ['http://122.15.211.126:80']
    for proxy in proxy_list:
        proxiess = {'http': proxy.strip()}
        for i in root:    
            s = HTMLSession()
            r = s.get(url,proxies=proxiess)
            r.html.render(timeout=20)
            
            try:
                product = {
                    'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
                    'price': r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text,
                    "stock": r.html.xpath('//*[@id="availability_feature_div"]',first=True).text
                }
                print(product)
            except:
                product = {'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
                            'price': "item Unavailable",
                            "stock": r.html.xpath('//*[@id="availability_feature_div"]',first=True).text
                            }
                print(product)
            return product
data = []
for root in roots:
    data.append(getprice(root))
df = pd.DataFrame(data)
df['price'] = df['price'].apply(lambda x: x.split(' ')[1])
df["price"] = df["price"].str.replace('Save:', '')
df["price"] = df["price"].str.replace('₹', '')
df["price"] = df["price"].str.replace(',', '')
df["price"] = df["price"].str.replace('"', '')
df.to_csv("scrapped_data.csv", index = False)