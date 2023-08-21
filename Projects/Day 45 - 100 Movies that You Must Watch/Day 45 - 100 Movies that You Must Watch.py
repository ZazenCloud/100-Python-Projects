from bs4 import BeautifulSoup
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
empire_webpage = response.text

# Create a BeautifulSoup object to parse the webpage
soup = BeautifulSoup(empire_webpage, "html.parser")

# Find all <h3> tags with class "title" and extract the text
tag_titles = soup.find_all(name="h3", class_="title")
titles = [title.getText() for title in tag_titles]

# Create a file and write the movie titles to it in reverse order (1 to 100)
with open("movies.txt", "w", encoding="utf-8") as file:
    for movie in titles[::-1]:
        file.write(movie + "\n")
