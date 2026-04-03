#!/usr/bin/env python3
"""
Result Parser Module
Parse export files into UI-ready dictionaries
Handles all metrics for Bootstrap UI display
"""

import json

def parse_export_data(export_file):
    """
    Parse export_TC06_fixed.json into UI-ready dict
    Returns nested dict with all metrics
    """
    try:
        with open(export_file, 'r') as f:
            data = json.load(f)

        return {
            'sust_kpis_dats': data.get('sust_kpis_dats', {}),
            'sust_kpis_no_dats': data.get('sust_kpis_no_dats', {}),
            'cost_revenue_dats': data.get('cost_revenue_dats', {}),
            'cost_revenue_no_dats': data.get('cost_revenue_no_dats', {}),
            'summary': _calculate_summary(data)
        }
    except FileNotFoundError:
        raise Exception(f"Export file not found: {export_file}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in export file: {str(e)}")

def parse_analytics_data(analytics_file):
    """
    Parse export_analysis_TC06_fixed.json for comparison
    Returns list of analytics items with original/converted/result
    """
    try:
        with open(analytics_file, 'r') as f:
            data = json.load(f)

        return {
            'analysis_dats_vs_no_dats': data,
            'summary': _calculate_analytics_summary(data)
        }
    except FileNotFoundError:
        raise Exception(f"Analytics file not found: {analytics_file}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in analytics file: {str(e)}")

def _calculate_summary(export_data):
    """Calculate summary metrics from export data"""
    total_cost_dats = _extract_total_cost(export_data.get('cost_revenue_dats', {}))
    total_cost_no_dats = _extract_total_cost(export_data.get('cost_revenue_no_dats', {}))

    # Extract productivity metrics
    productivity_dats = export_data.get('sust_kpis_dats', {}).get('productivity_', {})
    productivity_no_dats = export_data.get('sust_kpis_no_dats', {}).get('productivity_', {})

    # Extract environmental metrics
    environmental_dats = export_data.get('sust_kpis_dats', {}).get('fertiliser', {})
    water_dats = export_data.get('sust_kpis_dats', {}).get('water_', {})

    return {
        'total_cost_dats': total_cost_dats,
        'total_cost_no_dats': total_cost_no_dats,
        'cost_difference': total_cost_dats - total_cost_no_dats,
        'productivity_dats': productivity_dats,
        'productivity_no_dats': productivity_no_dats,
        'yield_dats': productivity_dats.get('yield', 0),
        'yield_no_dats': productivity_no_dats.get('yield', 0),
        'water_consumption': water_dats.get('water_consumption', 0),
        'irrigation_productivity': water_dats.get('irrigation_water_productivity', 0),
        'nitrogen_applied': environmental_dats.get('nitrogen_applied', 0),
        'ghg_emissions': environmental_dats.get('n2o_ghg_emission', 0)
    }

def _calculate_analytics_summary(analytics_data):
    """Calculate summary from analytics comparison data"""
    if not isinstance(analytics_data, dict):
        return {
            'total_comparisons': 0,
            'positive_differences': 0,
            'zero_differences': 0
        }

    positive_diff = 0
    zero_diff = 0
    total_comparisons = 0

    for sheet_name, sheet_data in analytics_data.items():
        if isinstance(sheet_data, dict):
            for category, category_data in sheet_data.items():
                if isinstance(category_data, dict):
                    for metric, value in category_data.items():
                        total_comparisons += 1
                        if value > 0:
                            positive_diff += 1
                        elif value == 0:
                            zero_diff += 1

    return {
        'total_comparisons': total_comparisons,
        'positive_differences': positive_diff,
        'zero_differences': zero_diff,
        'negative_differences': total_comparisons - positive_diff - zero_diff
    }

def _extract_total_cost(cost_data):
    """Extract total cost from cost analysis section"""
    try:
        cost_analysis = cost_data.get('cost_analysis', {})
        return float(cost_analysis.get('cost|tot_cost', 0))
    except (TypeError, ValueError, AttributeError):
        return 0.0
