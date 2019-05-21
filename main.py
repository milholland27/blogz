from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:doggo@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(500))

    def __init__(self, title, post):
        self.title = title
        self.post = post

#all blog posts
#@app.route('/blog')
#def index():
 #   all_blog_posts = Blog.query.all()
  #  return render_template('blog.html', posts=all_blog_posts)

#ind posts
@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        individualpost = Blog.query.get(post_id)
        return render_template('individualpost.html', individualpost=individualpost)

    else:
        all_blog_posts = Blog.query.all()
        return render_template('blog.html', posts=all_blog_posts)

#empty forms...

def empty_val(x):
    if x != "":
        return True
    else:
        return False
@app.route('/')
def redir_to_blog():
    return redirect('/blog')

@app.route('/newpost',  methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        title_error = ""
        blog_entry_error = ""
        
        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        post_new = Blog(post_title, post_entry)

        if empty_val(post_title) and empty_val(post_entry):
            print('says not empty')
            db.session.add(post_new)
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect (post_link)
        else:
            if not empty_val(post_title) and not empty_val(post_entry):
                title_error = "Enter Title for Blog"
                blog_entry_error = "Enter Blog Text"
                return render_template('newpost.html', blog_entry_error=blog_entry_error, title_error=title_error)

            elif not empty_val(post_title):
                title_error = "Enter Blog Title"
                return render_template('newpost.html', title_error=title_error, post_entry=post_entry)    
            elif not empty_val(post_entry):
                blog_entry_error = "Enter Text For Blog Entry"
                return render_template('newpost.html', blog_entry_error=blog_entry_error, post_title=post_title)
    #displays new blog entry form
    else:
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()