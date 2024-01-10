from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Ваши модели данных здесь

if __name__ == '__main__':
    app.run(debug=True)
