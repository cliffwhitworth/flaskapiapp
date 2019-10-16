# DB info
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'mysql_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'some_secret'
app.config['MYSQL_DATABASE_DB'] = 'flaskapiapp'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
mysql.init_app(app)
