import requests
import bs4
import re
from unicodedata import normalize

tipo = input("Digite a moeda (S - para sair): ")
while(tipo != "S" and tipo != "s"):
    content = requests.get("https://economia.uol.com.br/cotacoes/")
    content = content.text
    soup = bs4.BeautifulSoup(content, features="html.parser")
    titles = soup.select("h3")
    v_moeda = 0
    v_cresc = 0
    for t in titles:
        t = t.text
        t = normalize('NFKD', t).encode('ASCII', 'ignore').decode('ASCII')
        moeda = re.findall((r"\w*"+tipo+r"\w*"), t, re.IGNORECASE)
        if moeda:
            name = ''.join(moeda)

            v_moeda = re.findall(r"R\$.+", t)
            v_moeda = ''.join(v_moeda)

            v_cresc = re.findall(r"[\+|\-][0-9\,\. ]+\%", t)
            v_cresc = ''.join(v_cresc)

            print(name,"Comercial: ", v_moeda)
            print("Crescimento: ", v_cresc)
            break
    if(not titles or not moeda):
        print("Moeda não encontrada!\n")
    
    print("\n\n")
    tipo = input("Digite a moeda: ")
