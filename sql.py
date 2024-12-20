from dotenv import load_dotenv
import streamlit as st
import os
import mysql.connector
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide responses
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the MySQL database
def read_sql_query(sql, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION. \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this: SELECT * FROM STUDENT 
    WHERE CLASS='Data Science'; 
    The SQL code should not include any delimiters like ``` or the word `sql` in the output.
    """
]

# Streamlit App
st.set_page_config(page_title="I Can Retrieve Any SQL Query")
st.header("Gemini App To Retrieve SQL Data")

# Input question
question = st.text_input("Input: ", key="input")

# Submit button
submit = st.button("Ask the Question")

# MySQL database configuration
db_config = {
    "host": "localhost",       # Replace with your MySQL host
    "user": "root"
    ,   # Replace with your MySQL username
    "password": "", # Replace with your MySQL password
    "database": "spring"  # Replace with your MySQL database name
}

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print("Generated SQL Query:", response)
    
    # Execute SQL query
    result = read_sql_query(response, db_config)
    
    # Display response
    st.subheader("The Response is:")
    if result:
        for row in result:
            print(row)
            st.write(row)
    else:
        st.write("No results found or an error occurred.")
