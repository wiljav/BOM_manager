
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

:::mermaid

%%{init:{'theme': 'base', 'flowchart':{'nodeSpacing': 200}}}%%

graph TD
  subgraph Host
    A[Local Filesystem]
    A --> V1[./app -> /app/app]
    A --> V2[./data -> /app/data]
  end

  subgraph Docker Container: bom-app
    B1[Python\:3-slim]
    B2[Streamlit App]
    B3[DuckDB: bom.duckdb]
    B4[start\_streamlit\.sh]
    B5[Environment Variables]

    B1 --> B2
    B2 --> B3
    B2 --> B4
    B2 --> B5
  end

  subgraph User
    U[Browser]
  end
  
  U --> | localhost:8501 | B2
  U --> |  | A[Host]


:::


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
