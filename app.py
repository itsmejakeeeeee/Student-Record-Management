from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Default XAMPP MySQL user
app.config['MYSQL_PASSWORD'] = ''  # Default XAMPP MySQL password (empty by default)
app.config['MYSQL_DB'] = 'students_db'  # The database name

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')  # Fetch all students
    students = cur.fetchall()  # Get all rows from the query
    cur.close()
    return render_template('index.html', students=students)

# Add student route
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        course = request.form['course']
        
        # Insert the student data into the MySQL database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO students (name, email, age, course) VALUES (%s, %s, %s, %s)', (name, email, age, course))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        
        return redirect(url_for('home'))  # Redirect to home page after adding the student

    return render_template('add.html')

# Edit student route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students WHERE id = %s', (id,))
    student = cur.fetchone()  # Get the student with the given ID
    cur.close()
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        course = request.form['course']
        
        # Update the student data in the MySQL database
        cur = mysql.connection.cursor()
        cur.execute('UPDATE students SET name = %s, email = %s, age = %s, course = %s WHERE id = %s', 
                    (name, email, age, course, id))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        
        return redirect(url_for('home'))  # Redirect to home page after updating

    return render_template('edit.html', student=student)

# Delete student route
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students WHERE id = %s', (id,))
    student = cur.fetchone()  # Get the student with the given ID
    cur.close()

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    if request.method == 'POST':
        # Delete the student from the MySQL database
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM students WHERE id = %s', (id,))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        
        return redirect(url_for('home'))  # Redirect to home page after deletion
    
    return render_template('delete.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
