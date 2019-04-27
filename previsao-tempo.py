import re
import bs4
import requests
from unicodedata import normalize

'''
Autor: Luis Gustavo de Souza

Exercício para minerar informações de clima-tempo da página https://g1.globo.com/previsao-do-tempo/,
através do scrapy puro da página (sem utilização de API).
'''

entrada = input(
    "Pesquise a previsão do tempo da sua cidade (cidade e sigla do estado): ")

# Limpeza da entrada dos dados
cidade = re.findall(r"\w+", entrada)

cidade = ' '.join(cidade)
cidade = normalize('NFKD', cidade).encode('ASCII', 'ignore').decode(
    'ASCII')  # retira acentuacao das palavras
cidade = cidade.split(" ")

estado = cidade[-1]
cidade = cidade[0:-1]

estado = ''.join(estado).lower()
cidade = '-'.join(cidade).lower()

try:
    if len(cidade) >= 2:
        print("\nLoading...\n")
        content = requests.get(
            "https://g1.globo.com/previsao-do-tempo/"+estado+"/"+cidade+".ghtml")
        content = content.text

        soup = bs4.BeautifulSoup(content, features="html.parser")

        maxima = soup.select(".forecast-today__temperature--max")[0].text
        maxima = maxima[0:-4]

        minima = soup.select(".forecast-today__temperature--min")[0].text
        minima = minima[0:-4]

        table = soup.select(".forecast-table")[0].text

        print("\n\n\n\n\n\nLocalização: ", entrada, "\n")
        print("\t\t\tMáxima:", maxima, "\t", "Mínima:", minima, "\n")

        table = table.split("    ")
        table = [c.strip() for c in table if c != ""]
        lista = []
        raios = ""

        for t in table:
            text = re.findall(r"([0-9\%\: \/m{2}(km)h]+)", t)
            if re.findall(r"(?<=UV  Raios UV  )[A-záôóúéêãç]+", t):
                raios = re.findall(r"(?<=UV  Raios UV  ).+", t)
            text = [c.strip() for c in text]
            text = [c for c in text if len(c) > 1]
            if(text):
                lista.append(text)

    else:
        print("Entrada Inválida!")

    lista.append(raios)
    print(" -----------------------------------------------------------------------")
    print("| Prob. de chuva: ", lista[0][0], "-", lista[0]
          [1], "\t\t|\tVento: ", lista[3][0], "\t\t|")
    print("| Nascer do sol: ", lista[1][0],
          "\t\t|\tUmidade: ", lista[4][0], "\t\t|")
    print("| Pôr do sol: ", lista[2][0],
          "\t\t\t|\tRaios UV: ", lista[5][0], "\t|")
    print(" -----------------------------------------------------------------------")

except IndexError:
    print("Cidade Não Encontrada!")
