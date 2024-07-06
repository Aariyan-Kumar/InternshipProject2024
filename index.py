from flask import Flask, render_template, request
import pyodbc, logging

app = Flask(__name__)


def get_dbConnection():
    server = "LAPTOP-28STMO59"
    database = "InternshipProject2024"
    username = "sa"
    password = "Aariyan@77630"
    driver = "{ODBC Driver 17 for SQL Server}"

    try:
        connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(connection_string)
        logging.info("Database connection successful")
        return conn
    except pyodbc.InterfaceError as e:
        logging.error(f"Error connecting to the database: {e}")
        return None


@app.route("/")
def home():
    conn = get_dbConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE';"
    )
    tables = [row.table_name for row in cursor.fetchall()]
    conn.close()
    return render_template("index.html", tables=tables)

@app.route('/show_table', methods=['POST'])
def show_table():
    table = request.form["table"]
    conn = get_dbConnection()
    cursor = conn.execute(f"SELECT * FROM {table}")
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns,row)) for row in cursor.fetchall()]

    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE';"
    )
    tables = [row.table_name for row in cursor.fetchall()]
    conn.close()

    return render_template('index.html', tables = tables, data = data)

if __name__ == "__main__":
    app.run()
