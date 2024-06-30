from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Function to load blog posts from JSON file
def load_posts():
    try:
        with open('blog_posts.json', 'r') as f:
            posts = json.load(f)
    except FileNotFoundError:
        posts = []
    return posts

# Function to save blog posts to JSON file
def save_posts(posts):
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

# Function to fetch a single post by ID
def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_id = max((post['id'] for post in posts), default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content'],
            'likes': 0
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'GET':
        message = 'Please enter and submit'
        return render_template('update.html', post=post, message=message)

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        for post in posts:
            if post['id'] == post_id:
                post['author'] = author
                post['title'] = title
                post['content'] = content
                save_posts(posts)
                message = 'update successfull'
                return render_template('update.html', post=post, message=message)
        message = "Something went wrong. Try again!"
        return render_template('update.html', post=post, message=message)



@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    posts = load_posts()
    for post in posts:
        if post_id == post["id"]:
            post['likes'] += 1
            save_posts(posts)
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
