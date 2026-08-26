from flask import Flask, render_template, request
import os
import mssql_python

app = Flask(__name__)


def get_db_connection():
    connection_string = (
        f"Server={os.environ['DB_SERVER']};"
        f"Database={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USER']};"
        f"PWD={os.environ['DB_PASSWORD']};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

    return mssql_python.connect(connection_string)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        email = request.form["email"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Employees (Name, Department, Email)
            VALUES (?, ?, ?)
            """,
            (name, department, email)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Employee added successfully!"

    return render_template("add_employee.html")


if __name__ == "__main__":
    app.run(debug=True)