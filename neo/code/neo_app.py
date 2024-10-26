from flask import Flask, render_template, redirect, url_for
import pandas as pd
import os
import subprocess  # For calling other Python scripts

app = Flask(__name__)

# Load the NEO data
def load_neo_data():
    csv_file_path = '../data/processed_neo_data/neo_data_au_with_neo_class_diameter.csv'
    if os.path.exists(csv_file_path):
        return pd.read_csv(csv_file_path)
    return None

@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/summery')
def summery():
    neo_data = load_neo_data()
    total_neos = len(neo_data) if neo_data is not None else 0
    # Limit to only 5 rows for display
    neo_data_to_display = neo_data if neo_data is not None else None
    return render_template('summery.html', neo_data=neo_data_to_display.head(), total_neos=total_neos)

@app.route('/download')
def download():
    # Call your first Python script
    subprocess.run(['python', 'neo_download.py']) 
    return redirect(url_for('summery'))

@app.route('/process')
def process():
    # Call your second Python script
    subprocess.run(['python', 'neo_data_processor.py']) 
    return redirect(url_for('index'))

@app.route('/visualize')
def visualize():
    # Call your third Python script
    subprocess.run(['python', 'neo_data_visualization.py']) 
    return redirect(url_for('visualize'))

if __name__ == '__main__':
    app.run(debug=True)
