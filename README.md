
# 🔧 Modular BOM & Engineering Data Manager

A lightweight, local-first Bill of Materials and engineering data manager built with Streamlit + DuckDB.

## Features

- Upload CSV files dynamically and store them in DuckDB
- Add parts manually via form
- Export to Excel anytime
- Runs entirely inside Docker — no cloud needed
- Fully modular and extendable

---

## 🧰 Built With

- [Python](https://www.python.org/ )
- [DuckDB](https://duckdb.org/ ) – Fast in-process OLAP database
- [Typer](https://typer.tiangolo.com/ ) – For CLI interface
- [Pandas](https://pandas.pydata.org/ ) – Data manipulation
- [Openpyxl](https://openpyxl.readthedocs.io/ ) – Excel export support

---

## 🐳 Running with Docker (Recommended)

### Prerequisites

- Docker
- Docker Compose

### Build and Run

```bash
docker compose up --build
```

App will be available at:
👉 http://localhost:8501 (Streamlit UI)


### To stop
```bash
docker compose down
```
