import google.generativeai as genai
import sqlite3
api_key1='AIzaSyCEyKMGgq1VAkuoGAdyeZR3FcUHQSjKiKI'
api_key2="AIzaSyDAxglkJMZiptI5U7iiEajpbGi3DglgR2E"
genai.configure(api_key=api_key1)
class Bot():
    def __init__(self):
        self.model=genai.GenerativeModel('gemini-pro')
        self.db="database_adress"
        self.classifyprompt=[

            """your task is to classify the given text as a normal chat vs data request from the following db schema:
             -- Employees Table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    department_id INT,
    manager_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
);

-- Departments Table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- LeaveRequests Table
CREATE TABLE LeaveRequests (
    leave_request_id INT PRIMARY KEY,
    employee_id INT,
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    reason TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Attendance Table
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY,
    employee_id INT,
    date DATE,
    clock_in_time TIME,
    clock_out_time TIME,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- CalendarEvents Table
CREATE TABLE CalendarEvents (
    event_id INT PRIMARY KEY,

    event_name VARCHAR(100),
    start_datetime DATETIME,
    end_datetime DATETIME,
    description TEXT
);

-- TrainingPrograms Table
CREATE TABLE TrainingPrograms (
    program_id INT PRIMARY KEY,
    program_name VARCHAR(100),
    program_description TEXT,
    start_date DATE,
    end_date DATE
);

-- TrainingEnrollments Table
CREATE TABLE TrainingEnrollments (
    enrollment_id INT PRIMARY KEY,
    employee_id INT,
    program_id INT,
    enrollment_date DATE,
    completion_status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (program_id) REFERENCES TrainingPrograms(program_id)
);

-- Payroll Table
CREATE TABLE Payroll (
    payroll_id INT PRIMARY KEY,
    employee_id INT,
    pay_period_start_date DATE,
    pay_period_end_date DATE,
    gross_salary DECIMAL(10, 2),
    deductions DECIMAL(10, 2),
    net_salary DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- PerformanceMetrics Table
CREATE TABLE PerformanceMetrics (
    metric_id INT PRIMARY KEY,
    employee_id INT,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- HRAnalytics Table
CREATE TABLE HRAnalytics (
    analytics_id INT PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    date DATE
);/n
give me 2 if it is normal chat and give me 1 if it is request of info from the schema. give me only 2 or 1 .without any other characters and don't return None. 
            """
        ]
        self.english_qprompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the following schema:
   -- Employees Table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    department_id INT,
    manager_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
);

-- Departments Table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- LeaveRequests Table
CREATE TABLE LeaveRequests (
    leave_request_id INT PRIMARY KEY,
    employee_id INT,
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    reason TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Attendance Table
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY,
    employee_id INT,
    date DATE,
    clock_in_time TIME,
    clock_out_time TIME,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- CalendarEvents Table
CREATE TABLE CalendarEvents (
    event_id INT PRIMARY KEY,

    event_name VARCHAR(100),
    start_datetime DATETIME,
    end_datetime DATETIME,
    description TEXT
);

-- TrainingPrograms Table
CREATE TABLE TrainingPrograms (
    program_id INT PRIMARY KEY,
    program_name VARCHAR(100),
    program_description TEXT,
    start_date DATE,
    end_date DATE
);

-- TrainingEnrollments Table
CREATE TABLE TrainingEnrollments (
    enrollment_id INT PRIMARY KEY,
    employee_id INT,
    program_id INT,
    enrollment_date DATE,
    completion_status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (program_id) REFERENCES TrainingPrograms(program_id)
);

-- Payroll Table
CREATE TABLE Payroll (
    payroll_id INT PRIMARY KEY,
    employee_id INT,
    pay_period_start_date DATE,
    pay_period_end_date DATE,
    gross_salary DECIMAL(10, 2),
    deductions DECIMAL(10, 2),
    net_salary DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- PerformanceMetrics Table
CREATE TABLE PerformanceMetrics (
    metric_id INT PRIMARY KEY,
    employee_id INT,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- HRAnalytics Table
CREATE TABLE HRAnalytics (
    analytics_id INT PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    date DATE
);/n
you have to convert given instruction into sql statement according to the schema 
also the sql code should not have ``` in beginning or end and sql word in output



    """


        ]
        self.eng_response_prompt = [
        """
            I see you're an expert in understanding SQL queries! 
        I'll provide you with an SQL statement and its output. 
            Your task is to translate the sql statement and the result in simple English form \n\n
        For example,\nExample 1 - 
        SELECT COUNT(*) FROM randomtable ; : some random number 
        your output should be something like , There are five students.also don't include any info about the sql query just provide the result in normal form
    
    """
        ]
    def response(self,question,prompt):
        response=self.model.generate_content([prompt[0],question])
        return response.text
    def read_sql_query(self,sql,db):
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    def eng_response(self,question):
        
        response=self.response(question,self.english_qprompt)
        print(response)
        data=self.read_sql_query(response,self.db)
        english_res=self.response(str(response)+":"+str(data),self.eng_response_prompt)
        return english_res
    