"""CSV Data Explorer - Flask backend.

Single-folder layout: Flask serves the static files (index.html, app.js,
style.css) directly so the project can be uploaded and run as-is.

Endpoints:
    GET  /                -> the web app
    GET  /<static files>  -> app.js, style.css
    GET  /api/sample      -> profile of the bundled sample dataset
    POST /api/profile     -> profile of an uploaded CSV (multipart field "file")
"""
import io

import pandas as pd
from flask import Flask, jsonify, request, send_file

from analysis import profile_dataframe

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB upload cap


@app.get('/')
def index():
    return send_file('index.html')


@app.get('/<path:filename>')
def static_files(filename):
    if filename in ('app.js', 'style.css'):
        return send_file(filename)
    return 'Not found', 404


@app.get('/api/sample')
def sample():
    df = pd.read_csv('sample_orders.csv')
    return jsonify(profile_dataframe(df, name='sample_orders.csv'))


@app.post('/api/profile')
def profile():
    upload = request.files.get('file')
    if upload is None or upload.filename == '':
        return jsonify({'error': 'No file uploaded. Send a CSV as multipart field "file".'}), 400
    try:
        df = pd.read_csv(io.BytesIO(upload.read()))
    except Exception as exc:
        return jsonify({'error': f'Could not parse CSV: {exc}'}), 400
    if df.empty:
        return jsonify({'error': 'The CSV has no data rows.'}), 400
    return jsonify(profile_dataframe(df, name=upload.filename))


if __name__ == '__main__':
    app.run(debug=True)
