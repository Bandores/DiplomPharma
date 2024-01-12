from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand
from main import app, db

cli = FlaskGroup(app)

# Используйте FlaskCommand вместо Manager
migrate = Migrate(app, db)
cli.add_command('db', MigrateCommand)

if __name__ == "__main__":
    cli()
