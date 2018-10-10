from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the homepage!'

@app.route('/test')
def test():
    return '<h2>It\'s a test !</h2>'

@app.route('/profile/<username>')
def profile(username):
    return '<h1>Welcome %s</h1>' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return '<h1>Post ID is %s</h1>' % post_id

if __name__ == "__main__":
    apt.run(debug = True)