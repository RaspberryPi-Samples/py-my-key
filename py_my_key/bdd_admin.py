from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here

# Flask and Flask-SQLAlchemy initialization here

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))

app.run()