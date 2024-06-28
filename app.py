from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = {
            "title": request.form['title'],
            "author": request.form['author'],
            "content": request.form['content']
        }
        blog_posts = load_blog_posts()
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()
    if request.method == 'POST':
        blog_posts[post_id] = {
            "title": request.form['title'],
            "author": request.form['author'],
            "content": request.form['content']
        }
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    post = blog_posts[post_id]
    return render_template('update.html', post=post, post_id=post_id)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()
    if 0 <= post_id < len(blog_posts):
        del blog_posts[post_id]
        save_blog_posts(blog_posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
