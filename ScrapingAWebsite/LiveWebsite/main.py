from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, 'html.parser')
articles = soup.find_all(name="span", class_="titleline")
article_texts = [article_tag.getText() for article_tag in articles]
article_links = [article_tag.find(name='a').get("href") for article_tag in articles]

# Finding the upvotes
# If all articles on the page have upvotes, this will work:
# article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

# However, some submissions may not have any upvotes yet.
# This uses a conditional expression to handle cases where there are no upvotes (span is None)
subtexts = soup.findAll(class_="subtext")
article_upvotes = [int(line.span.span.getText().strip(" points")) if line.span.span else 0 for line in subtexts]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(
    f"Most upvoted article: {article_texts[largest_index]}\n"
    f"Number of upvotes: {article_upvotes[largest_index]} points\n"
    f"Available at: {article_links[largest_index]}"
)