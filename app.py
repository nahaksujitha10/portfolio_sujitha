# from flask import Flask, render_template, request, jsonify
# import os

# app = Flask(__name__, static_folder='static')

# if not os.path.exists('static/pdf'):
#     os.makedirs('static/pdf')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     try:
#         data = request.get_json()
#         name = data.get('name')
#         email = data.get('email')
#         subject = data.get('subject')
#         message = data.get('message')
        
#         # Here you can add email sending logic
#         # For now, we'll just return success
#         return jsonify({
#             'status': 'success',
#             'message': 'Message sent successfully!'
#         }), 200
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': str(e)
#         }), 500
    
# app = Flask(__name__, static_folder='static')

# if not os.path.exists('static/pdf'):
#     os.makedirs('static/pdf')

# if __name__ == '__main__':
#     app.run(debug=True) 





from flask import Flask, render_template, send_from_directory, send_file
import os

app = Flask(__name__, static_folder='static')

# Print the absolute path for debugging
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PDF_DIR = os.path.join(BASE_DIR, 'static', 'pdf')
print(f"PDF Directory: {PDF_DIR}")

# Ensure the pdf directory exists
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)
    print(f"Created PDF directory at: {PDF_DIR}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view-pdf')
def view_pdf():
    try:
        pdf_path = os.path.join(PDF_DIR, 'suji.pdf')
        print(f"Attempting to serve PDF from: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            print(f"PDF not found at: {pdf_path}")
            return "Error: PDF file not found. Please ensure 'suji.pdf' exists in the static/pdf directory", 404
            
        # Try direct file send
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=False,
            download_name='suji.pdf'
        )
    except Exception as e:
        print(f"Error serving PDF: {str(e)}")
        return f"Error serving PDF: {str(e)}", 500

@app.route('/static/pdf/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_DIR, filename)

@app.route('/debug-pdf')
def debug_pdf():
    pdf_path = os.path.join(PDF_DIR, 'suji.pdf')
    exists = os.path.exists(pdf_path)
    return f"PDF path: {pdf_path}<br>File exists: {exists}"

@app.errorhandler(404)
def page_not_found(e):
    return "404 Error - Page Not Found", 404

if __name__ == '__main__':
    # List contents of PDF directory on startup
    print("\nContents of PDF directory:")
    if os.path.exists(PDF_DIR):
        files = os.listdir(PDF_DIR)
        for file in files:
            print(f"- {file}")
    else:
        print("PDF directory does not exist!")
    
    app.run(debug=True) 