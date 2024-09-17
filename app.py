import pandas as pd
import json
from flask import Flask, render_template, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load Excel data and convert it to a hierarchical format
def load_and_process_excel(file_path):
    df = pd.read_excel(file_path)

    # Convert the Excel data into a nested dictionary format suitable for D3.js
    def build_hierarchy(df):
        hierarchy = {}

        # Loop through each row and create a hierarchical structure
        for _, row in df.iterrows():
            current_level = hierarchy
            for col in df.columns:
                if pd.isna(row[col]):
                    continue
                if row[col] not in current_level:
                    current_level[row[col]] = {}
                current_level = current_level[row[col]]
        
        return hierarchy

    hierarchy_data = build_hierarchy(df)
    return hierarchy_data

# Load and process Excel file
file_path = r'C:\Users\pragy\Thunder\Semiconductor- industries and experts (2).xlsx'
hierarchy_data = load_and_process_excel(file_path)

# Save the processed data as JSON
json_file = r'C:\Users\pragy\Thunder\hir_data.json'
with open(json_file, 'w') as f:
    json.dump(hierarchy_data, f)

# Flask route to serve the hierarchical data as JSON
@app.route('/data')
def get_data():
    with open(json_file) as f:
        data = json.load(f)
    return jsonify(data)

# Route to serve the HTML template for the D3.js visualization
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

