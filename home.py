from flask import Flask, render_template, request, redirect, session #iclude Flask class, render_template, request, redirect, and session
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

#session 'salt'
app.secret_key = 'asdf&&^(*ahasfljhas'

@app.route('/')
def index():
	#set up a cursor object, which is what the sql uses to connect and run queries
	cursor = mysql.connect().cursor()
	# execute out query
	cursor.execute("SELECT content FROM page_content WHERE page = 'home' AND location = 'header' AND status = '1'")
	header_text = cursor.fetchall()
	cursor2 = mysql.connect().cursor()
	# execute out query
	cursor2.execute("SELECT content, header_text, image_link FROM page_content WHERE page = 'home' AND location = 'left_block' AND status = '1' LIMIT 5")
	left_block_data = cursor2.fetchall()
	print header_text
	return render_template('index.html', data = left_block_data)
#=======================
#make a new route called admin
@app.route('/admin')
#define the method for the new route admin
def admin():
	#get the var "message" our of the query if it exists...
	if request.args.get('message'):
		#display if there is a message that the login failed
		return render_template('admin.html', message = 'Login failed')
	else:
		return render_template('admin.html')
#=======================
#new route, admin_gateway, acts as a gateway, if login is bad or good. Add method post so the form can get here.
@app.route('/admin_submit', methods=['GET', 'POST'])
#define the method for the new route
def admin_submit():
	print request.form
	if request.form['username'] == 'admin' and request.form['password'] == 'admin':
		#you may proceed
		#but before you do, let me give you a ticket
		session['username'] = request.form['username']
		return redirect('/admin_portal')
	else:
		#try again
		return redirct('/admin?message=login_failed')
	return request.form['username'] + ' ---- ' + request.form['password']

#new route after a successful login for admin
@app.route('/admin_portal')
#define the method for the new route
def admin_portal():
	#session variable 'username' exists in dictionary...proceed
	if 'username' in session:
		return render_template('admin_portal.html')
	#===================================
	#you have no ticket. no soup for you.
	else:
		return redirect('/admin?message=you must log in')
@app.route('/admin_update', methods=['POST'])
def admin_update():
	#first, do you belong here?
	if 'username' in session:
		#ok, they are logged in. i will insert your stuff...
		body = request.form['body_text']
		header = request.form['header']
		image = request.form['image']
		#set up a cursor object, which is what the sql uses to connect and run queries
		cursor = mysql.connect().cursor()
		query = "INSERT INTO page_content VALUES(DEFAULT, 'home', '"+body+"', 1, 1, 'left_block', NULL, '"+header+"', '"+image+"')"
		print query
		# execute out query
		# cursor.execute("INSERT INTO page_content VALUES(DEFAULT, 'home', '%s', 1, 1, 'left_block', NULL, '%s', '%s')" ) % body, header, image
		cursor.execute(query)

		return redirect('/admin_portal?success=Added')
	#===================================
	#you have no ticket. no soup for you.
	else:
		return redirect('/admin?message=you must log in')

if __name__ == "__main__":
	app.run(debug=True)