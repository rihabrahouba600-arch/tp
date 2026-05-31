import pandas as pd
import duckdb
from pathlib import Path

csv_path = Path("data/ventes.csv")
db_path = "ventes.duckdb"

df = pd.read_csv(csv_path)
con = duckdb.connect(db_path)
con.execute("CREATE OR REPLACE TABLE ventes_raw AS SELECT * FROM df")
con.close()

print("Ingestion terminée : ventes_raw créée dans DuckDB")