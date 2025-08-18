import mysql.connector
import os
'''
# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'certification_tracker')

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
'''

conn = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "39KZ8xro8WmzgLR.root",
  password = "E7UakFtZmhsBnXL7",
  database = "test",
  ssl_ca = "isrgrootx1.pem",
  ssl_verify_cert = True,
  ssl_verify_identity = True
)

cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS certification_tracker")

# Use the created database
cursor.execute(f"USE certification_tracker")

# Create the users table (with password field)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    user_type ENUM('student', 'teacher') NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create the courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
)
""")

# Create the teacher_student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teacher_student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    student_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_teacher_student (teacher_id, student_id)
)
""")

# Create the certificates table (fixed name from certifications)
cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates (
    certificate_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    certificate_name VARCHAR(255) NOT NULL,
    issue_date DATE NOT NULL,
    certificate_file VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
)
""")

# Insert some sample courses if they don't exist
cursor.execute("SELECT COUNT(*) FROM courses")
course_count = cursor.fetchone()[0]

if course_count == 0:
    sample_courses = [
        ('Python Programming', 'PY101', 'Introduction to Python programming language'),
        ('Web Development', 'WEB101', 'HTML, CSS, and JavaScript fundamentals'),
        ('Data Science', 'DS101', 'Introduction to data analysis and machine learning'),
        ('Database Management', 'DB101', 'SQL and database design principles'),
        ('Mobile App Development', 'MOB101', 'Creating mobile applications')
    ]
    
    cursor.executemany(
        "INSERT INTO courses (course_name, course_code, description) VALUES (%s, %s, %s)",
        sample_courses
    )

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Database setup completed successfully!")
