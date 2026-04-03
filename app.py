#!/usr/bin/env python3
"""
Assessment Tool Flask Application
Provides Bootstrap UI for file upload, selection, and results display
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
import logging
from classes.calculation_wrapper import run_calculation
from classes.result_parser import parse_export_data, parse_analytics_data
import threading

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

calculation_lock = threading.Lock()

UPLOAD_FOLDER = './InputTCs'
OUTPUT_FOLDER = './Outputs'
ALLOWED_EXTENSIONS = {'json'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_json_structure(data):
    required_fields = ['testcaseNumber', 'cultivationType', 'datsInformation', 'yearlyAssessmentInformation']
    return all(field in data for field in required_fields)

def is_calculation_running():
    return calculation_lock.locked()

def get_cultivation_years_for_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception:
        return None

    yearly_info = data.get('yearlyAssessmentInformation', [])
    years = []
    for entry in yearly_info:
        if isinstance(entry, dict) and 'cultivationYear' in entry:
            years.append(entry['cultivationYear'])
    return years

@app.route('/')
def index():
    files = get_available_files()
    return render_template('index.html',
                         files=files,
                         calculation_running=is_calculation_running())

@app.route('/files')
def get_files():
    files = get_available_files()
    return jsonify({'files': files})

@app.route('/cultivation-years/<filename>')
def get_cultivation_years(filename):
    years = get_cultivation_years_for_file(filename)
    if years is None:
        return jsonify({'success': False, 'error': 'File not found or invalid JSON'}), 404
    return jsonify({'success': True, 'years': years})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Only JSON files allowed'})

    try:
        content = file.read()
        data = json.loads(content)

        if not validate_json_structure(data):
            return jsonify({
                'success': False,
                'error': 'Invalid JSON structure. Required fields: testcaseNumber, cultivationType, datsInformation, yearlyAssessmentInformation'
            })

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        return jsonify({
            'success': True,
            'message': f'File {filename} uploaded successfully',
            'filename': filename
        })

    except json.JSONDecodeError:
        return jsonify({'success': False, 'error': 'Invalid JSON format'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/calculate/<filename>', methods=['POST'])
def calculate(filename):
    logger.info(f"Starting calculation for file: {filename}")
    
    if is_calculation_running():
        logger.warning("Calculation already in progress")
        return jsonify({
            'success': False,
            'error': 'Calculation already in progress. Please wait.',
            'already_running': True
        })

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    logger.debug(f"Checking file path: {filepath}")
    
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return jsonify({'success': False, 'error': f'File {filename} not found'})

    calculation_lock.acquire()

    try:
        tc_name = filename.rsplit('.', 1)[0]
        logger.info(f"Running calculation for test case: {tc_name}")

        cultivation_year = None
        if request.is_json:
            cultivation_year = request.json.get('cultivationYear')
        else:
            cultivation_year = request.form.get('cultivationYear')

        if cultivation_year is None or str(cultivation_year).strip() == "":
            return jsonify({
                'success': False,
                'error': 'Cultivation year is required'
            })

        result = run_calculation(tc_name, str(cultivation_year).strip())
        logger.debug(f"Calculation result: {result}")

        if result['success']:
            logger.info(f"Calculation completed successfully for {tc_name}")
            return jsonify({
                'success': True,
                'message': 'Calculation completed',
                'tc_name': tc_name,
                'redirect': url_for('results', filename=filename)
            })
        else:
            error_msg = result.get('error', 'Unknown error occurred')
            logger.error(f"Calculation failed for {tc_name}: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg,
                'error_details': result.get('error_details')
            })

    except Exception as e:
        logger.exception(f"Unexpected error during calculation: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })
    finally:
        calculation_lock.release()
        logger.debug("Calculation lock released")

@app.route('/results/<filename>')
def results(filename):
    tc_name = filename.rsplit('.', 1)[0]
    export_file = os.path.join(app.config['OUTPUT_FOLDER'], f'export_{tc_name}.json')
    analytics_file = os.path.join(app.config['OUTPUT_FOLDER'], f'export_analysis_{tc_name}.json')

    if not os.path.exists(export_file):
        return render_template('error.html',
                           message=f'Export file not found for {filename}. Run calculation first.')

    if not os.path.exists(analytics_file):
        return render_template('error.html',
                           message=f'Analytics file not found for {filename}. Run calculation first.')

    export_data = parse_export_data(export_file)
    analytics_data = parse_analytics_data(analytics_file)

    return render_template('results.html',
                         filename=filename,
                         tc_name=tc_name,
                         export_data=export_data,
                         analytics_data=analytics_data)

@app.route('/download/<file_type>/<filename>')
def download_file(file_type, filename):
    tc_name = filename.rsplit('.', 1)[0]

    if file_type == 'export':
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], f'export_{tc_name}.json')
    elif file_type == 'analytics':
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], f'export_analysis_{tc_name}.json')
    else:
        return jsonify({'error': 'Invalid file type'})

    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'})

def get_available_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.json'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            files.append({
                'name': filename,
                'size': os.path.getsize(filepath),
                'modified': os.path.getmtime(filepath)
            })

    files.sort(key=lambda x: x['modified'], reverse=True)
    return files

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000)
