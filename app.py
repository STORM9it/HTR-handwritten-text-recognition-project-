from distutils.log import debug
from fileinput import filename
from flask import *
from flask_mysqldb import MySQL
import easyocr
app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sql123@python'
app.config['MYSQL_DB'] = 'HTR'
mysql = MySQL(app)

@app.route('/contact', methods=['POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        # Create cursor
        cur = mysql.connection.cursor()
        
        # Execute query
        cur.execute("INSERT INTO response(name, email, subject, message) VALUES(%s, %s, %s, %s)", (name, email, subject, message))
        
        # Commit to database
        mysql.connection.commit()
        
        # Close connection
        cur.close()
        
        return 'Thanks for your feedback!'
    
    return render_template('index.html') 
  
@app.route('/')  
def main():  
    return render_template("index.html") 
@app.route('/about')  
def about():  
    return render_template("about.html")  
@app.route('/contact')  
def contact():  
    return render_template("contact.html")   
  
@app.route('/', methods = ['POST']) 
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        reader = easyocr.Reader(['en']) 
        result = reader.readtext(f.filename, detail = 0, paragraph=True)

        return render_template("index.html", name = result)  
  
if __name__ == '__main__':  
    app.run(port=81, debug=False)