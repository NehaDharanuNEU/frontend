from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pytesseract
from PIL import Image
from fpdf import FPDF
import os
import traceback
import pytesseract

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path for your system

app = Flask(__name__)
CORS(app)

# Root route
@app.route('/')
def home():
    return "Welcome to the Image to Text PDF Converter API!"

# /convert route
@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    if 'image' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save the uploaded image temporarily
        temp_path = f"temp_{image_file.filename}"
        image_file.save(temp_path)

        # Perform OCR on the image
        text = pytesseract.image_to_string(Image.open(temp_path))

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)

        # Save PDF
        output_path = "output.pdf"
        pdf.output(output_path)

        # Clean up the temporary image file
        os.remove(temp_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        traceback.print_exc()  # Log the full error stack trace
        return jsonify({"error": str(e)}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
