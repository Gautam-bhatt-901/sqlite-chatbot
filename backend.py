from flask import Flask, request, jsonify, render_template
import sqlite3
import nltk
# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

app = Flask(__name__)

# Function to query the SQLite database
def query_database(sql_query, params=()):
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    cursor.execute(sql_query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Preprocess user input
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words.remove("after")
    lemmatizer = WordNetLemmatizer()

    # remove stopwords and apply lemmatization
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return filtered_tokens

# Function to extract Department name from user query
def extract_department(words):
    departments = ["sales", "engineering", "marketing", "hr"] #known departments
    for word in words:
        if word in departments:
            return word    
    return None    

# Function to process user queries
def process_query(user_input):
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_input)  # YYYY-MM-DD format
    extracted_date = date_match.group(0) if date_match else None

    words = preprocess_text(user_input)
    # identify Intent and execute sql query
    if "employee" in words and "department" in words:
        department = extract_department(words)
        if department:
            sql = "SELECT Name FROM Employees WHERE LOWER(Department) = LOWER(?)"
            result = query_database(sql, (department,))
            return f"Employees in {department}: " + ", ".join([row[0] for row in result]) if result else "No Employees found."
        
    elif "manager" in words and "department" in words:
        department = extract_department(words)
        if department:
            sql = "SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER(?)"
            result = query_database(sql, (department,))
            return f"Manager of {department}: {result[0][0]}" if result else "Department Not found."
            
    elif "hired" in words and "after" in words:
        if extracted_date:
            sql = "SELECT Name FROM Employees WHERE Hire_Date > DATE(?)"
            result = query_database(sql, (extracted_date,))
            return f"Employees hired after {extracted_date}: " + ", ".join([row[0] for row in result]) if result else "No Employees found."
        
    elif "salary" in words and "expense" in words:
        department = extract_department(words)
        if department:
            sql = "SELECT SUM(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)"
            result = query_database(sql, (department,))
            return f"Total Salary expense for {department}: ₹{result[0][0]}" if result[0][0] else "Department not found."
    return "Sorry i couldn't understand your query. Please ask something else."

# API Endpoint
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods = ["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    response = process_query(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug = True) 