-- Question 1: Creating a database for students as requested.
-- ID's must be unique and the primary key of the table
-- Phone number is mandatory as well as unique. Email is also required to be unique if available

CREATE TABLE students(
	student_id SERIAL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	homeroom_number INTEGER UNIQUE NOT NULL,
	email VARCHAR(250) UNIQUE,
	phone VARCHAR(250) UNIQUE NOT NULL,
	grad_year INTEGER NOT NULL
)

-- Same thing for teachers 
CREATE TABLE teachers(
	teacher_id SERIAL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
    homeroom_number INTEGER UNIQUE NOT NULL,
	email VARCHAR(250) UNIQUE,
	phone VARCHAR(250) UNIQUE NOT NULL
)

-- Question 2: inserting values into the table Students
INSERT INTO students(
	first_name,
	last_name,
	homeroom_number,
	phone,
	grad_year
)
VALUES
	('Mark','Watney',5,'777-555-1234',2035)

-- Same as before, for table Teachers
INSERT INTO teachers(
	first_name,
	last_name,
	homeroom_number,
	department,
	email,
	phone
)
VALUES
	('Jonas','Salk',5,'Biology','jsalk@school.org','777-555-4321')