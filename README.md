
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
- [Pandas](https://pandas.pydata.org/ ) – Data manipulation
- [Openpyxl](https://openpyxl.readthedocs.io/ ) – Excel export support

---

## Architecture




---

## 🌱 Directory tree:

```sh
.
├── app
│   ├── bom_tab.py
│   ├── construction_tab.py
│   ├── database.py
│   ├── lab_samples_tab.py
│   ├── main.py
│   ├── manual_entry_tab.py
│   ├── materials_tab.py
│   └── utils.py
├── CSV_data
│   ├── bom.csv
│   └── project_materials.csv
├── data
│   └── bom.duckdb
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── start_streamlit.sh
```

---

## 🐳 Running with Docker

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
