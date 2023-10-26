from bs4 import BeautifulSoup
import requests  # To send a request to any website
import pandas as pd  # In pandas, we work with dataframes which is the equivalent of tables in Excel

years = ['1930', '1934', '1938', '1950', '1954', '1958', '1962', '1966', '1970', '1974', '1978', '1982', '1986', '1990',
         '1994', '1998', '2002', '2006', '2010', '2014', '2018']


def get_matches(year):
    if(year == '2022'):
        web = 'https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup'
    else:
        web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'  # fstring allows us to use variables inside a string
    response = requests.get(web)  # get is a method of the library requests
    # print(response.text)  # Printing the text of the response # The HTML of the website is printed

    content = response.text
    # We're gonna parse the content # lxml is a parser
    soup = BeautifulSoup(content, 'lxml')
    # soup helps us extract data from the website
    # soup is a BeautifulSoup object

    # Look for pattern in the HTML file
    # Find tag and class name

    # find() matches only the first element
    # find_all() finds all the elements which matches the 'tag' and 'class'

    # Syntax
    # soup.find_all(tag, class_= 'name')
    # soup.find(tag, class_='name')

    # Storing all the matches in a list
    matches = soup.find_all('div', class_='footballbox')

    # matches is a list of soups
    # match represents a soup
    # We can't extract data without a soup

    # 3 empty lists
    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find('th', class_='fhome').get_text())  # appending the name of the home team into the list
        score.append(match.find('th', class_='fscore').get_text())  # appending the score into the list
        away.append(match.find('th', class_='faway').get_text())  # appending the name of the away team into the list

    # To store the extracted data into a table we use pandas

    dict_football = {'home': home, 'score': score, 'away': away}
    # The 'home' key stores the home list as it's value
    df_football = pd.DataFrame(dict_football)  # Storing the dict_football dictionary in a pandas dataframe as df_football
    df_football['year'] = year  # Creating a new column named year
    return df_football


# print(get_matches('1982'))

fifa = []  # List of dataframes
for year in years:
    fifa.append(get_matches(year))  # get_matches(year) returns a dataframe which gets appended to the list

# The above code snippet can be replaced by
# fifa = [get_matches(year) for year in years]

# We're gonna concatenate all the dataframes into one final dataframe
df_fifa = pd.concat(fifa, ignore_index=True)  # The second parameter ignores the index of each dataframe
# Exporting the final dataframe to a csv file
df_fifa.to_csv('FIFA_WC_Historical_Data.csv', index=False)  # The index no. won't be imported to the csv file

# Fixture 2022
df_fixture = get_matches('2022')  # Dataframe which stores the 2022 WC fixture data
df_fixture.to_csv('FIFA_WC_2022_Fixture.csv', index=False)
