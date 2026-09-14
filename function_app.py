import azure.functions as func
import logging
import os
import pyodbc

app = func.FunctionApp()

@app.route(route="GetStatus", auth_level=func.AuthLevel.ANONYMOUS)
def GetStatus(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Capstone API: checking database connectivity.')

    try:
        conn_str = os.environ["SQL_CONNECTION_STRING"]
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        conn.close()
        return func.HttpResponse(
            f"Capstone API is live. Database connection successful.\nSQL Server version: {row[0][:50]}...",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"Capstone API is live, but database connection failed: {str(e)}",
            status_code=500
        )
