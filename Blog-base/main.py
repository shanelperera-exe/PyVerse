from flask import Flask, render_template
from post import Post
import requests

posts_url = "https://api.npoint.io/c790b4d5cab58020d391"
blog_response = requests.get(url=posts_url)
blog_response.raise_for_status()
posts = blog_response.json()

post_objects = [Post(post['id'], post['title'], post['subtitle'], post['body']) for post in posts]

app = Flask(__name__)
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for post in post_objects:
        if post.id == index:
            requested_post = post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
