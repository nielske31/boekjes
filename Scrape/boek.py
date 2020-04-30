import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
# dit is de uitgekleede link als je zoekt op orlando virginia woolf
page = 1
my_url="https://www.boekwinkeltjes.nl/s/?q=orlando+virginia+woolf&p=" + str(page)
df = pd.DataFrame(columns = ["auteur", "titel"]) # create a dataframe


while True:
    # getting the page and parsing it to soup (something like that)
    page_soup = soup(requests.get(my_url).text, "html.parser")
    table = page_soup.find(class_="table-responsive") #gets the table

    if table == None:
        break# als table leeg is, dwz geen (extra?) resultaten, stop met zoeken

    print("looking at page: " + str(page))

    rows = table.findAll("tr") #gets all the rows from the table

    # pak een rij uit de tabel
    for i in rows:
            data = {} #maak een lege dictionary die gevuld gaat worden met rij data
            poep = i.findAll(class_="table-text")
            if poep: #kijkt of de lijst gevuld is !
                data["auteur"] = poep[0].text
                titel = poep[1].text
                if "meer info" in titel:
                    titel = titel[17:-34] #haalt de whitespaces aan begin en eind weg
                else:
                    titel = titel[17:-12]
                data["titel"] = titel
                data["bijzonderheden"] = i.findAll(class_="extra")[1].text
                data["prijs"] = i.find(class_="price").select("strong")[0].text #Kan dit anders?/sneller?

                plaatje = i.find(class_="order").find("a").find("img") #haalt het plaatje op
                if plaatje == None: #als er geen plaatje is staat de winkelnaam in de text
                    winkelnaam = i.find(class_="order").find("a").text
                else: # anders in de alt
                    winkelnaam = plaatje.get("alt")
                    if winkelnaam.endswith(" button"): #soms staat er button achter
                        winkelnaam = winkelnaam[:-7] #strip button
                data["winkelnaam"] = winkelnaam

                df = df.append(data, ignore_index = True)


    page +=1
    my_url="https://www.boekwinkeltjes.nl/s/?q=orlando+virginia+woolf&p=" + str(page)

# df.to_csv("DATA.csv", sep = "\t") # Dit doet het niet goed.
print(df, sep="\n")