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
    response = model.generate_content([prompt, question])
    return response.text

# Function to retrieve column names from the database
def get_column_names(db_config, table_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        conn.close()
        return columns
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []

# Function to retrieve query results from the database
def read_sql_query(sql, db_config):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []

# Streamlit app
st.set_page_config(page_title="Dynamic Gemini SQL Query App")
st.header("Gemini App To Retrieve SQL Data Dynamically")

# Initialize session state
if "db_config" not in st.session_state:
    st.session_state.db_config = None
if "columns" not in st.session_state:
    st.session_state.columns = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None

# Database connection form
st.subheader("Database Connection Details")
host = st.text_input("Host", value="localhost")
user = st.text_input("User", value="root")
password = st.text_input("Password", type="password")
database = st.text_input("Database Name")
table_name = st.text_input("Table Name")

if st.button("Connect to Database"):
    db_config = {"host": host, "user": user, "password": password, "database": database}
    columns = get_column_names(db_config, table_name)
    
    if columns:
        st.session_state.db_config = db_config
        st.session_state.columns = columns
        column_list = ", ".join(columns)
        st.session_state.prompt = f"""
        You are an expert in converting English questions to SQL queries!
        The SQL database has the name {table_name.upper()} and has the following columns: {column_list}.
        For example:
        Example 1 - How many entries of records are present?, 
        the SQL command will be something like this: SELECT COUNT(*) FROM {table_name.upper()};
        Example 2 - Tell me all the students studying in Data Science class?, 
        the SQL command will be something like this: SELECT * FROM {table_name.upper()} 
        WHERE CLASS='Data Science';
        The SQL code should not include any delimiters like ``` or the word `sql` in the output.
        """
        st.success(f"Connected to {database}. Retrieved columns: {', '.join(columns)}")
    else:
        st.error("Could not retrieve columns. Check your connection details and table name.")

# If connection is established, proceed with query generation
if st.session_state.db_config and st.session_state.columns:
    st.subheader("Generate SQL Query")
    question = st.text_input("Ask a Question")
    
    if st.button("Generate SQL Query"):
        response = get_gemini_response(question, st.session_state.prompt)
        st.write("Generated SQL Query:", response)
        
        # Execute SQL query
        result = read_sql_query(response, st.session_state.db_config)
        
        st.subheader("Query Results")
        if result:
            for row in result:
                st.write(row)
        else:
            st.write("No results found or an error occurred.")
