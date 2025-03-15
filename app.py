from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Persistent storage directory
STORAGE_DIR = "/yash_PV_dir"

@app.route('/sum', methods=['POST'])
def calculate_sum():
    data = request.get_json()

    if not data or 'file' not in data or not data['file'] or 'product' not in data or not data['product']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data['product']
    file_path = os.path.join(STORAGE_DIR, file_name)

    try:
        if not os.path.isfile(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404

        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        if len(rows) < 2:
            return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

        headers = [h.strip().lower() for h in rows[0]]
        if headers != ["product", "amount"]:
            return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

        total_sum = 0
        for row in rows[1:]:
            if len(row) != 2:
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

            try:
                product_name = row[0].strip()
                amount = float(row[1].strip())

                if product_name.lower() == product.lower():
                    total_sum += amount
            except ValueError:
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

        return jsonify({"file": file_name, "sum": int(total_sum)}), 200

    except Exception as e:
        return jsonify({"file": file_name, "error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)