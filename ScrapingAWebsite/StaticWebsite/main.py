from bs4 import BeautifulSoup
import requests

response = requests.get("https://appbrewery.github.io/news.ycombinator.com/")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

articles = soup.find_all(name="a", class_="storylink")
article_texts = [article_tag.getText() for article_tag in articles]
article_links = [article_tag.get("href") for article_tag in articles]
article_upvotes = [int(upvote.getText().split(" ")[0]) for upvote in soup.find_all(name="span", class_="score")]

highest_upvote = max(article_upvotes)
highest_upvote_index = article_upvotes.index(highest_upvote)

print(f"Title: {article_texts[highest_upvote_index]}")
print(f"Links: {article_links[highest_upvote_index]}")
print(f"Upvotes: {highest_upvote}")