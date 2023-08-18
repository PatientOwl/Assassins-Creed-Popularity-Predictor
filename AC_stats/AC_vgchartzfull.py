'''


'''
from bs4 import BeautifulSoup, element # 'element' is a temporary element for sub_soup
from datetime import datetime
import urllib.request
import pandas as pd
import numpy as np

# setting up columns with empty arrays
pages = 19
rec_count = 0
rank = []
game_name = []
platform = []
year = []
genre = []
critic_score = []
user_score = []
publisher = []
developer = []
sales_na = []
sales_pal = []
sales_jp = []
sales_ot = []
sales_gl = []
last_updated = []

# Scraping all games with the name "Assassin's Creed" from the GameDB 
# table found on vgchartz.com
urlhead = 'https://www.vgchartz.com/gamedb/?page='
urltail = '&name=Assassin%27s+Creed&console=&region=All&developer=&publisher=&genre=&boxart=Both&ownership=Both'
urltail += '&results=1000&order=Game&showtotalsales=1&showtotalsales=1&showpublisher=1'
urltail += '&showpublisher=1&showvgchartzscore=0&shownasales=1&showdeveloper=1&showcriticscore=1'
urltail += '&showpalsales=1&showpalsales=1&showreleasedate=1&showuserscore=1&showjapansales=1'
urltail += '&showlastupdate=1&showothersales=1&showgenre=1&sort=GL'

# cycles through each page of the GameDB results with a for loop
for page in range(1, pages):
    surl = urlhead + str(page) + urltail #page.content
    r = urllib.request.urlopen(surl).read() #opens URL, reads it, and returns the HTML string, becoming the page.content
    soup = BeautifulSoup(r, "html.parser") 
    print(f"Page: {page}")

    # searching for <a> tags with game urls to get the name of the game 
    # using list(filter(lambda x:)) to filter for each 'href' (URL) attribute (or the link element)
    # 'href' stands for hyperlink reference
    # converting filtered lambda x (<a> href tag) into a list
    game_tags = list(filter(
        lambda x: 'href' in x.attrs and x.attrs['href'].startswith('https://www.vgchartz.com/game/'),
        soup.find_all("a")
    ))
    #################################
    # Retrieving data for each game #
    #################################
    for tag in game_tags:

        # adding game name to game_name[] list
        # splitting the string name of game, joining them as one string,
        # and then appending to game_name array
        game_name.append(" ".join(tag.string.split()))

        # print that it is fetching the game
        print(f"{rec_count + 1} Fetch data for game {game_name[-1]}")

        ################################
        # Getting different attributes #
        ################################

        # using .parent to traverse up the DOM tree from the game name <a>
        data = tag.parent.parent.find_all("td")

        # filling last_update[]
        # reformatting the timestamp of 'Last Update' column on website
        check_update = ' '.join(data[14].string.split())
        
        # different format for the full date
        if check_update == 'N/A':
            last_updated.append('N/A')

        if 'st' in check_update:
            formatted_update = check_update.replace('st', '')
            dateString = formatted_update
            dateTimeObj = datetime.strptime(dateString, "%d %b %y")
            last_updated.append(dateTimeObj)
            
        if 'nd' in check_update:
            formatted_update = check_update.replace('nd', '')
            dateString = formatted_update
            dateTimeObj = datetime.strptime(dateString, "%d %b %y")
            last_updated.append(dateTimeObj)
            
        if 'rd' in check_update:
            formatted_update = check_update.replace('rd', '')
            dateString = formatted_update
            dateTimeObj = datetime.strptime(dateString, "%d %b %y")
            last_updated.append(dateTimeObj)
            
        if 'th' in check_update:
            formatted_update = check_update.replace('th', '')
            dateString = formatted_update
            dateTimeObj = datetime.strptime(dateString, "%d %b %y")
            last_updated.append(dateTimeObj)
            
        # filling platform[]
        platform.append(data[3].find('img').attrs['alt'])

        # filling publisher[]
        publisher.append(data[4].string)

        # filling developer[]
        developer.append(data[5].string)

        # filling critic_score[]
        critic_score.append(
            float(data[6].string) if
            not data[6].string.startswith("N/A") else np.nan)

        # filling user_score[]
        user_score.append(
            float(data[7].string) if
            not data[7].string.startswith("N/A") else np.nan)

        # filling sales_na[]
        sales_na.append(
            float(data[9].string[:-1]) if
            not data[9].string.startswith("N/A") else np.nan)

        # filling sales_pal[]
        sales_pal.append(
            float(data[10].string[:-1]) if
            not data[10].string.startswith("N/A") else np.nan)

        # filling sales_jp[]
        sales_jp.append(
            float(data[11].string[:-1]) if
            not data[11].string.startswith("N/A") else np.nan)

        # filling sales_ot[]
        sales_ot.append(
            float(data[12].string[:-1]) if
            not data[12].string.startswith("N/A") else np.nan)

        # filling sales_gl[]
        sales_gl.append(
            float(data[8].string[:-1]) if
            not data[8].string.startswith("N/A") else np.nan)

        # filling year[]
        release_year = data[13].string.split()[-1]
        # different format for year
        if release_year.startswith('N/A'):
            year.append('N/A')
        else:
            if int(release_year) >= 80:
                year_to_add = np.int32("19" + release_year)
            else:
                year_to_add = np.int32("20" + release_year)
            year.append(year_to_add)

        # filling genre[]
        # going to every individual website to get genre info
        url_to_game = tag.attrs['href']
        site_raw = urllib.request.urlopen(url_to_game).read()
        sub_soup = BeautifulSoup(site_raw, "html.parser")

        # the info box is inconsistent among games so we have to find 
        # all the <h2>s and traverse from that to the genre name,
        # since 'Genre' is an <h2> tag
        h2s = sub_soup.find("div", {"id": "gameGenInfoBox"}).find_all('h2')
        
        # making a temporary tag here to search for the <h2> that contains
        # the word "Genre"
        temp_tag = element.Tag
        for h2 in h2s:
            if h2.string == 'Genre':
                temp_tag = h2
        genre.append(temp_tag.next_sibling.string)

        # recording score of how many total games have been fetched
        rec_count += 1

columns = {
    #'Rank': rank,
    'Last Updated': last_updated,
    'Name': game_name,
    'Platform': platform,
    'Year': year,
    'Genre': genre,
    'Critic_Score': critic_score,
    'User_Score': user_score,
    'Publisher': publisher,
    'Developer': developer,
    'NA_Sales': sales_na,
    'PAL_Sales': sales_pal,
    'JP_Sales': sales_jp,
    'Other_Sales': sales_ot,
    'Global_Sales': sales_gl
}
print(rec_count)

df = pd.DataFrame(columns)
print(df.columns)
df = df[[
    'Last Updated', 'Name', 'Platform', 'Year', 'Genre',
    'Publisher', 'Developer', 'Critic_Score', 'User_Score',
    'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]
df.to_csv("AC_vgsales.csv", sep=",", encoding='utf-8', index=False)