import requests
import bs4

req = requests.get("http://g1.globo.com/")
content = req.text
s = bs4.BeautifulSoup(content)

spans = s.find_all("h1")
for lines in spans:
    print(lines)
