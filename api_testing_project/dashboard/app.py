"""
Flask Dashboard Application for Automated API Testing
Provides web interface to run tests and view results
"""

import os
import json
import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, jsonify, request, send_file
from config.config import (
    FLASK_HOST, FLASK_PORT, FLASK_DEBUG, REPORT_FOLDER,
    VALID_CITIES, OPENWEATHERMAP_API_KEY, BASE_URL
)

app = Flask(__name__, template_folder='templates', static_folder='static')

BASE_DIR    = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
REPORTS_DIR = os.path.join(PROJECT_ROOT, REPORT_FOLDER)

try:
    os.makedirs(REPORTS_DIR, exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create reports folder: {e}")

test_results = {
    'status': 'idle',
    'total_tests': 0,
    'passed_tests': 0,
    'failed_tests': 0,
    'skipped_tests': 0,
    'duration': 0.0,
    'timestamp': None,
    'results_by_category': {},
    'all_tests': [],
    'test_output': ''
}


def get_test_count_by_category():
    categories = {
        'unit':        os.path.join(PROJECT_ROOT, 'tests', 'test_unit.py'),
        'functional':  os.path.join(PROJECT_ROOT, 'tests', 'test_functional.py'),
        'negative':    os.path.join(PROJECT_ROOT, 'tests', 'test_negative.py'),
        'edge':        os.path.join(PROJECT_ROOT, 'tests', 'test_edge.py'),
        'performance': os.path.join(PROJECT_ROOT, 'tests', 'test_performance.py')
    }
    counts = {}
    for category, test_file in categories.items():
        try:
            if os.path.exists(test_file):
                with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    counts[category] = f.read().count('def test_')
            else:
                counts[category] = 0
        except Exception:
            counts[category] = 0
    return counts


def parse_test_results(output):
    test_results_list = []
    lines = output.split('\n')
    for line in lines:
        # Match Windows-style paths too: tests\test_unit.py::test_name PASSED
        pattern = r'(tests[\\/]test_\w+\.py::[\w\[\]-]+)\s+(PASSED|FAILED|SKIPPED|ERROR)'
        match = re.search(pattern, line)
        if match:
            test_path = match.group(1).replace('\\', '/')
            status    = match.group(2)

            if   'test_unit'        in test_path: category = 'unit'
            elif 'test_functional'  in test_path: category = 'functional'
            elif 'test_negative'    in test_path: category = 'negative'
            elif 'test_edge'        in test_path: category = 'edge'
            elif 'test_performance' in test_path: category = 'performance'
            else:                                 category = 'other'

            test_name = test_path.split('::')[-1] if '::' in test_path else test_path
            test_results_list.append({
                'name': test_name,
                'path': test_path,
                'category': category,
                'status': status
            })
    return test_results_list


def run_pytest_with_json_report():
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        report_file_path = os.path.join(REPORTS_DIR, 'report.html')

        start_time = datetime.now()

        cmd = [
            sys.executable, '-m', 'pytest',
            os.path.join(PROJECT_ROOT, 'tests'),
            '-v',
            '--tb=short',
            f'--html={report_file_path}',
            '--self-contained-html',
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=180,
            cwd=PROJECT_ROOT
        )

        duration = (datetime.now() - start_time).total_seconds()
        output   = process.stdout + '\n' + process.stderr

        # ── CORRECT PARSING using regex on the summary line ──
        # pytest summary line looks like: "45 passed, 12 failed in 18.3s"
        passed_match  = re.search(r'(\d+) passed',  output)
        failed_match  = re.search(r'(\d+) failed',  output)
        skipped_match = re.search(r'(\d+) skipped', output)
        error_match   = re.search(r'(\d+) error',   output)
        duration_match= re.search(r'in\s+([\d.]+)s', output)

        passed_count  = int(passed_match.group(1))  if passed_match  else 0
        failed_count  = int(failed_match.group(1))  if failed_match  else 0
        skipped_count = int(skipped_match.group(1)) if skipped_match else 0
        error_count   = int(error_match.group(1))   if error_match   else 0
        duration_val  = float(duration_match.group(1)) if duration_match else duration

        # Combine errors into failed
        failed_count  = failed_count + error_count
        total_tests   = passed_count + failed_count + skipped_count

        # DEBUG — visible in your terminal
        print("=" * 50)
        print("PYTEST OUTPUT (last 400 chars):")
        print(output[-400:])
        print(f"PARSED  →  passed={passed_count}  failed={failed_count}  skipped={skipped_count}  total={total_tests}  duration={duration_val}s")
        print("=" * 50)

        # Parse individual test rows
        test_details = parse_test_results(output)

        # Count per category
        categories = {
            'unit':        {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0},
            'functional':  {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0},
            'negative':    {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0},
            'edge':        {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0},
            'performance': {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0},
        }
        for test in test_details:
            cat    = test['category']
            status = test['status']
            if cat in categories:
                categories[cat]['total'] += 1
                if   status == 'PASSED':  categories[cat]['passed']  += 1
                elif status == 'FAILED':  categories[cat]['failed']  += 1
                elif status == 'SKIPPED': categories[cat]['skipped'] += 1

        return {
            'passed':      passed_count,
            'failed':      failed_count,
            'skipped':     skipped_count,
            'total':       total_tests,
            'duration':    duration_val,
            'return_code': process.returncode,
            'output':      output,
            'test_details': test_details,
            'categories':  categories
        }

    except subprocess.TimeoutExpired:
        print("ERROR: Tests timed out after 180 seconds")
        return {'passed':0,'failed':0,'skipped':0,'total':0,'duration':0,'return_code':-1,'output':'Timeout','test_details':[],'categories':{}}
    except Exception as e:
        print(f"ERROR running pytest: {e}")
        return {'passed':0,'failed':0,'skipped':0,'total':0,'duration':0,'return_code':-1,'output':str(e),'test_details':[],'categories':{}}


@app.route('/')
def index():
    test_counts = get_test_count_by_category()
    return render_template('index.html',
                           test_counts=test_counts,
                           total_available_tests=sum(test_counts.values()))


@app.route('/run-tests', methods=['POST'])
def run_tests():
    global test_results
    try:
        test_results['status']    = 'running'
        test_results['timestamp'] = datetime.now().isoformat()

        results = run_pytest_with_json_report()

        test_results['total_tests']          = results['total']
        test_results['passed_tests']         = results['passed']
        test_results['failed_tests']         = results['failed']
        test_results['skipped_tests']        = results['skipped']
        test_results['duration']             = results['duration']
        test_results['status']               = 'completed'
        test_results['results_by_category']  = results['categories']
        test_results['all_tests']            = results['test_details']
        test_results['test_output']          = results['output']

        # Save to file
        try:
            results_file = os.path.join(REPORTS_DIR, 'results.json')
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(test_results, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save results.json: {e}")

        response_data = {
            'status':               test_results['status'],
            'total':                test_results['total_tests'],
            'passed':               test_results['passed_tests'],
            'failed':               test_results['failed_tests'],
            'skipped':              test_results['skipped_tests'],
            'duration':             test_results['duration'],
            'timestamp':            test_results['timestamp'],
            'results_by_category':  test_results['results_by_category'],
            'all_tests':            test_results['all_tests'],
            'message': f"✅ {test_results['passed_tests']} Passed | ❌ {test_results['failed_tests']} Failed"
        }
        print(f"SENDING RESPONSE: total={response_data['total']} passed={response_data['passed']} failed={response_data['failed']}")
        return jsonify(response_data)

    except Exception as e:
        print(f"ROUTE ERROR: {e}")
        test_results['status'] = 'failed'
        return jsonify({
            'status': 'failed', 'error': str(e),
            'total': 0, 'passed': 0, 'failed': 0,
            'skipped': 0, 'duration': 0, 'all_tests': [],
            'results_by_category': {}
        }), 500


@app.route('/results', methods=['GET'])
def get_results():
    return jsonify({
        'status':               test_results['status'],
        'total':                test_results['total_tests'],
        'passed':               test_results['passed_tests'],
        'failed':               test_results['failed_tests'],
        'skipped':              test_results['skipped_tests'],
        'duration':             test_results['duration'],
        'timestamp':            test_results['timestamp'],
        'results_by_category':  test_results['results_by_category'],
        'test_counts':          get_test_count_by_category()
    })


@app.route('/report')
def view_report():
    try:
        report_file = os.path.join(REPORTS_DIR, 'report.html')
        if os.path.exists(report_file):
            return render_template('report.html', report_exists=True,  report_file='/reports/report.html')
        else:
            return render_template('report.html', report_exists=False, report_file=None)
    except Exception as e:
        return render_template('report.html', report_exists=False, report_file=None, error=str(e)), 500


@app.route('/reports/<filename>')
def serve_report(filename):
    try:
        file_path = os.path.join(REPORTS_DIR, filename)
        if not os.path.abspath(file_path).startswith(os.path.abspath(REPORTS_DIR)):
            return jsonify({'error': 'Invalid file'}), 403
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download-report')
def download_report():
    try:
        report_file = os.path.join(REPORTS_DIR, 'report.html')
        if os.path.exists(report_file):
            return send_file(
                report_file, mimetype='text/html', as_attachment=True,
                download_name=f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            )
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/status')
def get_status():
    return jsonify({
        'status':         test_results['status'],
        'test_counts':    get_test_count_by_category(),
        'last_run':       test_results['timestamp'],
        'api_configured': bool(OPENWEATHERMAP_API_KEY),
        'total_tests':    test_results['total_tests'],
        'passed':         test_results['passed_tests'],
        'failed':         test_results['failed_tests']
    })


@app.route('/api-details')
def get_api_details():
    return jsonify({
        'api_key_configured': bool(OPENWEATHERMAP_API_KEY and len(OPENWEATHERMAP_API_KEY) > 4),
        'base_url':           BASE_URL,
        'valid_test_cities':  VALID_CITIES
    })


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("  Automated API Testing Dashboard")
    print("=" * 60)
    print(f"  URL  →  http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"  Root →  {PROJECT_ROOT}")
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG, use_reloader=False)