from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from flask_cors import CORS  # For cross-browser compatibility
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing

@app.route('/')
def index():
    try:
        # Create response with CSP header to block external scripts/extensions
        response = make_response(render_template('index.html'))
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none';"
        )
        return response
    except Exception as e:
        logging.error(f"Error rendering index: {str(e)}")
        return "Error loading page", 500

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return jsonify({'error': 'Division by zero is not allowed'})
            result = num1 / num2
        else:
            return jsonify({'error': 'Invalid operation'})

        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in calculation: {str(e)}")
        return jsonify({'error': str(e)}), 400

# Serve favicon from static folder
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/x-icon')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to port 5001