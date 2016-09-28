from flask import Flask, render_template
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
#create an instance of the mysql class
mysql = MySQL()
#add to the app (Flask object) some config data for our connection
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
#The name of the database we want to connect to at the DB server
app.config['MYSQL_DATABASE_DB'] = 'disney'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# user the mysql object's method "init_app" and pass it the flask object
mysql.init_app(app)

@app.route('/')
def index():
	#set up a cursor object, which is what the sql uses to connect and run queries
	cursor = mysql.connect().cursor()
	# execute out query
	cursor.execute("SELECT content FROM page_content WHERE page = 'home' AND location = 'header' AND status = '1'")
	header_text = cursor.fetchall()
	print header_text
	return render_template('index.html', header = header_text)

@app.route('/admin')
def admin():
	return render_template('admin.html')

if __name__ == "__main__":
	app.run(debug=True)