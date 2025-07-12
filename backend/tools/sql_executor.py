import pandas as pd
import duckdb
"""
def run_sql_query(sql: str):
    df = pd.read_excel("backend/personality_datasert.xlsx")

    try:
        con = duckdb.connect()
        con.register("data", df)
        result = con.execute(sql).fetchdf()
        return result.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
"""
import pandas as pd
import duckdb
import os

def run_sql_query(query: str):
    # Load dataset — make sure the correct path is used
    dataset_path = os.path.join("backend", "personality_datasert.xlsx")
    
    try:
        # Load Excel into Pandas
        df = pd.read_excel(dataset_path)

        # Connect to DuckDB and register the DataFrame with the correct table name
        con = duckdb.connect()
        con.register("personality", df)  # ✅ Register as 'personality'

        # Execute the query and return result
        result = con.execute(query).fetchall()
        return result

    except Exception as e:
        return {"error": str(e)}
