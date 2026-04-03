#!/usr/bin/env python3
"""
Dynamic TC Name Runner
Temporarily modifies main.py tc_name before execution
"""

import sys
import os
import subprocess

def run_with_tc_name(tc_name):
    """
    Execute main.py with tc_name as command line argument
    """
    try:
        print(f"Running main.py with tc_name: {tc_name}")
        return True

    except Exception as e:
        print(f"Error preparing main.py execution: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tc_name = sys.argv[1]
        cultivation_year = sys.argv[2] if len(sys.argv) > 2 else None
        if run_with_tc_name(tc_name):
            # Execute main.py with tc_name (and optional cultivation_year) as argument
            cmd = [sys.executable, "main.py", tc_name]
            if cultivation_year is not None:
                cmd.append(str(cultivation_year))
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"main.py exited with code: {result.returncode}")
                sys.exit(result.returncode)
    else:
        print("Usage: python3 run_with_tc.py <tc_name> [cultivation_year]")
