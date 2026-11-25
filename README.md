# CSV Data Explorer (Python Flask + Pandas)

A web app that profiles any CSV file: upload a file and instantly get column
types, missing-value counts, numeric summaries, top values, correlations, and
a data preview. Built for analysts who want a first look at a dataset without
writing code.

## Features

- Upload any CSV (up to 10 MB) or explore the bundled sample dataset
- Per-column profile: data type, missing count and %, unique values, top values
- Numeric summary: mean, median, standard deviation, min, max
- Strongest pairwise correlations, sorted by |r|
- First-10-rows preview
- The profiling logic (`analysis.py`) is pure pandas and reusable in notebooks

## Tech stack

- **Backend:** Python, Flask, Pandas
- **Frontend:** HTML, CSS, vanilla JavaScript (fetch API)
- Single-folder layout so the project runs exactly as uploaded

## Project layout

```
app.py              Flask app and API routes
analysis.py         profiling logic (pure pandas)
index.html / app.js / style.css   frontend
sample_orders.csv   500-row synthetic dataset
requirements.txt    Python dependencies
```

## Run it locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## API

- `GET /api/sample` - profile of the bundled sample dataset
- `POST /api/profile` - profile of an uploaded CSV (multipart field `file`)

## Notes

- The bundled dataset is synthetic. Uploaded files are processed in memory and
  never stored on the server.
- Tested locally with Flask 3 and Python 3.11.
