# DATS Assessment Engine

The DATS Assessment Engine builds on the Quantifarm DATS assessment framework and aims to enable both quantitative and qualitative assessment of DATSs under real-world conditions.  The tool is conceived as a reusable, stand-alone software application that takes as input a set of ground-truth data (e.g. use of agricultural inputs, monetary costs, labour effort), feeds these into assessment algorithms, and produces numeric values for a predefined set of performance indicators. It can be downloaded and executed locally on a personal computer and provides a graphical user interface to facilitate data import and result visualization.

The tool offers both **CLI** and **Web Interface** usage modes.

## Table of Contents

- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [CLI Tool](#cli-tool)
- [Technical Overview](#technical-overview)
- [Repository Layout](#repository-layout)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)

## Technologies

<p align="center">
  The following Technologies / APIs / Libraries are utilised:
  <br>
  Python 3 : <a href="https://docs.python.org/3/"><strong>Explore Python 3.6+ docs »</strong></a>
  Flask : <a href="https://flask.palletsprojects.com/"><strong>Flask Web Framework »</strong></a>
  Bootstrap 5 : <a href="https://getbootstrap.com/"><strong>Bootstrap UI Framework »</strong></a>
</p>

## Installation

1. **Prerequisites**: Make sure to have [Python 3.6+](https://www.python.org/downloads/) installed

2. **Install Flask dependencies** (required for web interface):
   ```bash
   pip3 install --break-system-packages Flask Werkzeug
   ```

3. **Virtual Environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install Flask Werkzeug
   ```

## Usage

### Web Interface

The Flask application provides a user-friendly Bootstrap 5 UI for running calculations.

**Start the Flask app:**
```bash
python3 app.py
```

**Access the web interface:**
Open http://localhost:5000 in your browser

#### Web Interface Features

- **File Upload**: Upload JSON test case files to InputTCs/ folder
- **File Selection**: Select from available test case files
- **Blocking Calculation**: Only one calculation can run at a time (prevents concurrent jobs)
- **Results Display**: View all metrics in organized Bootstrap 5 tabs
- **JSON Downloads**: Download both export and analytics results

#### Web Interface Usage

1. **Upload New Test Case**
   - Click "Upload New File" section
   - Click "Upload File"
   - File is validated and saved to InputTCs/

2. **Select Existing File**
   - Choose from dropdown in "Select Test Case File" section
   - Click "Calculate Results"
   - Calculation runs with loading spinner (blocking - cannot start new job until complete)
   - Automatically redirected to results page

3. **View Results**
   
   Results page displays four tabs:
   
   **KPIs DATS** - Sustainability KPIs with DATS
   - Productivity metrics (yield, labour productivity)
   - Efficiency metrics
   - Quality metrics
   - Environmental metrics (fertiliser, water, electricity)
   - Social metrics

   **KPIs NO DATS** - Sustainability KPIs without DATS
   - Same categories as DATS for comparison

   **Cost Analysis** - Financial comparison
   - DATS costs vs NO DATS costs
   - Revenue comparison
   - Total cost difference calculation

   **Analytics** - Detailed comparison (DATS vs NO DATS)
   - Shows all 68+ formula comparisons
   - Color-coded by result (positive = green, zero = gray, negative = red)
   - Shows original formula, converted formula, and final result
   - Summary statistics (total comparisons, positive differences)

4. **Download Results**
   
   Click download buttons at top of results page:
   - **Export JSON**: Main export file (`export_TCXX.json`)
   - **Analytics JSON**: Analytics comparison file (`export_analysis_TCXX.json`)

### CLI Tool

The original CLI tool remains fully functional for command-line usage.

**Basic Usage:**
```bash
python3 main.py
```

This will list available JSON files in `InputTCs/` and prompt you to select one.

**Optional Flags:**
```bash
python3 main.py --debug  # Enable debug output
```

**Direct Dataset Selection:**
Pass the dataset name directly (without `.json`) to skip the prompt:
```bash
python3 main.py TC10_For_Testing_purposes
```

#### CLI Usage Steps

1. Place your front-end JSON export in `InputTCs/` (see the examples in that folder)
2. Run the evaluator with one of the methods above
3. Read the output JSON in `Outputs/`

## Technical Overview

The tool processes calculations through the following pipeline:

1. **Input Processing**: Reads user input JSON files from `InputTCs/`
2. **Mapping**: Uses `SteppingHelpers/mappings.json` to map form fields to Excel cell references
3. **Formula Extraction**: Extracts formulas from the Excel template in `Resources/` using `extract_formulas.vbs`
4. **Formula Conversion**: Converts the Excel formulas to Pythonic expressions into `ConvertedFormulas/ALL_toJSON.json`
5. **Calculation**: Evaluates the converted formulas and writes results to `Outputs/`

## Repository Layout

- `InputTCs/`: Front-end form exports (user input JSON)
- `Resources/`: Excel template (e.g., `Calculator_DEF_TC6_onion_FIXED.xlsx`)
- `SteppingHelpers/mappings.json`: Form-field-to-Excel-cell mapping
- `ExcelFormulaOutputs/`: Extracted Excel formulas (from VBScript)
- `ConvertedFormulas/ALL_toJSON.json`: Converted formulas in JSON
- `Outputs/`: Final computed results in JSON
- `extract_formulas.vbs`: VBScript to extract formulas from Excel
- `convert_formulas_to_json.py`: Converts extracted formulas to JSON/Pythonic expressions
- `main.py`: CLI evaluator (calculates formulas and produces output JSON)
- `app.py`: Flask web application
- `classes/`: Utility classes and modules
- `templates/`: HTML templates for web interface

## File Structure

```
/
├── main.py                    # CLI Tool
├── app.py                     # Flask application
├── run_with_tc.py             # Dynamically passes tc_name to CLI
├── classes/
│   ├── calculation_wrapper.py # Wraps CLI execution for Flask
│   ├── result_parser.py       # Parses results for UI
│   └── ...                    # Other utility classes
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   └── error.html
├── InputTCs/                  # Uploaded/test case files
├── Outputs/                   # All calculation results (both exports)
├── SteppingHelpers/           # Debug and helper files
├── ConvertedFormulas/         # Formula definitions
└── Resources/                 # Excel templates
```

## Testing

**Test CLI directly:**
```bash
python3 main.py TCXX
```

**Test calculation wrapper:**
```bash
python3 classes/calculation_wrapper.py TCXX
```

Expected wrapper response:
```json
{
  "success": true,
  "tc_name": "TCXX",
  "export_file": "./Outputs/export_TCXX.json",
  "analytics_file": "./Outputs/export_analysis_TCXX.json",
  "message": "Calculation completed successfully"
}
```

## Troubleshooting

**Port 5000 in use?**
```bash
lsof -i :5000
```
Kill the process if needed.

**Files not uploading?**
Check JSON structure has required fields:
- `testcaseNumber`
- `cultivationType`
- `datsInformation`
- `yearlyAssessmentInformation`

**Calculation fails?**
Check logs and ensure:
- Input file exists in InputTCs/
- Formula files exist in ConvertedFormulas/
- Mappings file exists in SteppingHelpers/

**Debug Mode:**
- For Flask: Set `debug=True` in `app.py` (line 176)
- For CLI: Use `--debug` flag