from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    with open('blog_posts.json') as f:
        return json.load(f)


def save_posts(posts):
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


def save_post(post):
    blog_posts = load_posts()
    blog_posts.append(post)
    save_posts(blog_posts)


def fetch_post_by_id(post_id):
    blog_posts = load_posts()
    for post in blog_posts:
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
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        new_post = {
            'id': len(load_posts()) + 1,  # Auto increment ID
            'author': author,
            'title': title,
            'content': content
        }
        save_post(new_post)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)  # Use save_posts instead of save_post
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
