from flask import Flask
from routes import api,auth
# from flask_migrate import Migrate
# from models.User import db

app = Flask(__name__)
app.config.from_object('config')

# db.init_app(app)
# migrate = Migrate(app, db)


app.register_blueprint(api.api, url_prefix='/api')
app.register_blueprint(auth.auth, url_prefix='/auth')


if __name__ == '__main__':
    #app.debug = True
    app.run()