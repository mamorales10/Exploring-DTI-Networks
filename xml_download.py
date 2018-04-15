import requests

URL1 = "https://www.ebi.ac.uk/Tools/hmmer/download/1AA0F0E8-36E1-11E8-B496-4E98DBC3747A."
URL2 = "/score?format=xml"

i = 1

while (i <= 346):
    response = requests.get(URL1 + str(i) + URL2)
    file = open('file%i.txt' %i, 'w')
    file.write(response.content)
    file.close()
    i = i + 1


