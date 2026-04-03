#!/usr/bin/env python3
"""
Calculation Wrapper Module
Wraps main.py execution to allow dynamic tc_name parameter
Preserves all CLI functionality while allowing Flask to trigger calculations
"""

import sys
import os
import json
import subprocess
import time
import logging
import re

def _extract_cli_error(stdout, stderr):
    combined = ""
    if stderr:
        combined += stderr
        if not combined.endswith("\n"):
            combined += "\n"
    if stdout:
        combined += stdout

    errors = []
    decoder = json.JSONDecoder()
    index = 0
    while index < len(combined):
        brace_index = combined.find("{", index)
        if brace_index == -1:
            break
        try:
            obj, end = decoder.raw_decode(combined[brace_index:])
            if isinstance(obj, dict) and "error" in obj:
                errors.append(obj["error"])
            index = brace_index + end
        except Exception:
            index = brace_index + 1

    if not errors:
        return None

    for item in errors:
        if isinstance(item, list):
            return item

    return errors[-1]

def run_calculation(tc_name, cultivation_year):
    """
    Execute main.py calculation for specified testcase file
    Returns: dict with success/error status
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting calculation wrapper for {tc_name}")
    
    try:
        # Check if input file exists
        input_file = f"./InputTCs/{tc_name}.json"
        if not os.path.exists(input_file):
            return {
                "success": False,
                "tc_name": tc_name,
                "error": f"Input file {tc_name}.json not found in InputTCs/"
            }

        # Use run_with_tc.py to dynamically modify main.py tc_name before execution
        logger.debug(f"Running subprocess: python run_with_tc.py {tc_name} {cultivation_year}")
        result = subprocess.run(
            [sys.executable, "run_with_tc.py", tc_name, str(cultivation_year)],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=300
        )

        logger.debug(f"Subprocess return code: {result.returncode}")
        logger.info(f"Subprocess stdout: {result.stdout}")
        logger.warning(f"Subprocess stderr: {result.stderr}")

        if result.returncode != 0:
            cli_error = _extract_cli_error(result.stdout, result.stderr)
            if cli_error:
                if isinstance(cli_error, list):
                    error_msg = "Calculation failed due to input errors"
                else:
                    error_msg = str(cli_error)
            else:
                error_msg = f"Calculation failed with return code {result.returncode}"
            
            logger.error(error_msg)
            return {
                "success": False,
                "tc_name": tc_name,
                "error": error_msg,
                "error_details": cli_error if isinstance(cli_error, list) else None,
                "stderr": result.stderr,
                "stdout": result.stdout
            }

        # Verify output files were created
        export_file = f"./Outputs/export_{tc_name}.json"
        analytics_file = f"./Outputs/export_analysis_{tc_name}.json"

        if not os.path.exists(export_file):
            return {
                "success": False,
                "tc_name": tc_name,
                "error": f"Export file not generated: {export_file}"
            }

        if not os.path.exists(analytics_file):
            return {
                "success": False,
                "tc_name": tc_name,
                "error": f"Analytics file not generated: {analytics_file}"
            }

        return {
            "success": True,
            "tc_name": tc_name,
            "export_file": export_file,
            "analytics_file": analytics_file,
            "message": "Calculation completed successfully"
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "tc_name": tc_name,
            "error": "Calculation timed out (5 minutes)"
        }
    except Exception as e:
        return {
            "success": False,
            "tc_name": tc_name,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = run_calculation(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python calculation_wrapper.py <tc_name>")
        print("Example: python calculation_wrapper.py TC06_fixed")
