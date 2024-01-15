import requests
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/forms/"

page = requests.get(url)
print(page)
soup = BeautifulSoup(page.text, 'html.parser')

# Getting the heading of the Teams
get_heading = soup.find_all("th")
for get_headings in get_heading:
    print(get_headings.text.strip())

print("\n")

# Getting by team
get_team = soup.find_all("tr", class_ = "team")
for get_teams in get_team:

    get_name = get_teams.find("td", class_ = "name")
    print(get_name.text.strip())

    get_year = get_teams.find("td", class_ = "year")
    print(get_year.text.strip())

    get_wins = get_teams.find("td", class_="wins")
    print(get_wins.text.strip())

    get_losses = get_teams.find("td", class_="losses")
    print(get_losses.text.strip())

#print(soup.find('p', class_ = "lead").text.strip()) #.find = extract the specific element, .find_all = extract all that contains sa same element
#print(soup.find_all('th'))
