import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

def main():
    response = requests.get(url=URL)
    response.raise_for_status()
    web_page = response.text

    soup = BeautifulSoup(web_page, "html.parser")
    movie_titles = get_movie_titles(soup)
    write_to_file(movie_titles)

def get_movie_titles(soup):
    movies = soup.find_all(name="h3", class_="title")
    movie_titles = [movie.getText() for movie in movies]
    movie_titles.reverse()
    return movie_titles

def write_to_file(lines):
    with open("movies.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

if __name__ == "__main__":
    main()

