import re;
import os;
import sys;
import argparse;
import json as JSON;
import numbers;
from classes.customFunctions import customFunctions;
from classes.amTools import amTools;

arg_parser = argparse.ArgumentParser(
    description = "Quantifarm assessment tool evaluator",
);
arg_parser.add_argument(
    "tc_name",
    nargs   = "?",
    default = None,
    help    = "InputTCs JSON filename without extension (e.g., TC10_Test_POLIMI)",
);
arg_parser.add_argument(
    "cultivationYear",
    nargs   = "?",
    default = None,
    help    = "Select Cultivation Year",
);
arg_parser.add_argument(
    "--debug",
    action  = "store_true",
    help    = "Enable debug output",
);
args = arg_parser.parse_args();


debug                  = True if args.debug else False;
loop                   = True;
loop_analytics         = True;
debug_Globals          = True;
debug_missingVariables = False;
amTool                 = amTools();

amTool.logv( "INFO" , amTool.text( "FAIL", "------------------------------------------" ) );
amTool.logv( "INFO" , amTool.text( "FAIL", "----  Company: NEUROPUBLIC            ----" ) );
amTool.logv( "INFO" , amTool.text( "FAIL", "----  Application: Assessment Tool    ----" ) );
amTool.logv( "INFO" , amTool.text( "FAIL", "----  Version: 1.8.11                 ----" ) );
amTool.logv( "INFO" , amTool.text( "FAIL", "----  Version Release: 2026-01-01     ----" ) );
amTool.logv( "INFO" , amTool.text( "FAIL", "----  Developer: amanos.dev@gmail.com ----" ) );
amTool.logv( "INFO" , amTool.text( "FAIL", "------------------------------------------" ) );

globals()[ "custom" ]  = {};
totalProcessedValues   = {};
processedValues        = {};
missing_variables      = set();
myAnalysisResultObject = {};

def clearAllLogs():
    with open( "./SteppingHelpers/replacements.txt", 'w' ) as file:
        pass;

    with open( "./SteppingHelpers/globals.txt", 'w' ) as file:
        pass;

    with open( "./SteppingHelpers/globals.txt", 'w' ) as file:
        pass;

def printGlobals( startingStringIndex = None ):
    if startingStringIndex is None : 
        startedGlobals = True;
    else:
        startedGlobals = False;

    with open( "./SteppingHelpers/globals.txt", 'w' ) as file:
        for variable in globals()[ "custom" ] : 
            if variable == startingStringIndex  :
                startedGlobals = True;

            if startedGlobals is True : 
                string = str( variable ) + " : " + str( globals()[ "custom" ][ variable ] );
                file.write( string + "\n");

def createMemoryObject( dataset , cultivationYear ):
    # Move Properties 
    # crop = dataset[ "yearlyAssessmentInformation" ][ 1 ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "parcelInformation" ][ "productType" ];
    crop = None;
    for data in dataset[ "yearlyAssessmentInformation" ]:
        if "parcelComparison" in data and len( data[ "parcelComparison" ] ) > 0:
            crop = data[ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "parcelInformation" ][ "productType" ];

    if crop is None :
        return { "error" : "No Crop Defined in JSON" };

    print( "Crop for Assessment : " + str( crop ) );
    print( "Cultivation Year : " + str( cultivationYear ) );

    globals()[ "custom" ][ "crop" ] = crop;
    cultivationYearIndex = 0;
    for index , year in enumerate( dataset[ "yearlyAssessmentInformation" ] ):
        if str( year[ "cultivationYear" ] ) == str( cultivationYear ):
            cultivationYearIndex = index;
    
    errors = [];

    for parent in [ "parcelAssessmentWithDATS" , "parcelAssessmentWithoutDATS" ]:

        # Add the Marketinfo to each DATS and NoDATS
        if "marketInformation" in dataset[ "yearlyAssessmentInformation" ][ cultivationYearIndex ] : 
            for marketEntity in dataset[ "yearlyAssessmentInformation" ][ cultivationYearIndex ][ "marketInformation" ] : 
                myConcat = ( "marketInformation_" + marketEntity ).lower();
                try :
                    myValue  = dataset[ "yearlyAssessmentInformation" ][ cultivationYearIndex ][ "marketInformation" ][ marketEntity ];
                    if myValue.isnumeric() : 
                        globals()[ "custom" ][ myConcat ] = float( myValue );
                    else:
                        globals()[ "custom" ][ myConcat ] = myValue;
                except( Exception ) as error :
                    globals()[ "custom" ][ myConcat ] = float( myValue );
                    # errors.append( "Problematic Property : [ " + str( marketEntity ) + " ] in 'marketInformation'" );
        else:
            errors.append( "Missing 'marketInformation' from JSON for year : '" + str( cultivationYear ) + "'" );

        # Add the datsInformation to each DATS and NoDATS
        for datProperty in dataset[ "datsInformation" ][ 0 ] : 
            myConcat = ( parent + "_datsInformation_" + datProperty ).lower();
            try :
                myValue  = dataset[ "datsInformation" ][ 0 ][ datProperty ];
                if myValue :
                    if myValue.isnumeric() : 
                        globals()[ "custom" ][ myConcat ] = float( myValue );
                    else:
                        globals()[ "custom" ][ myConcat ] = myValue;
                else:
                    errors.append( "Null value in [ " + str( datProperty ) + " ] of DAT" );
            except( Exception ) as error :
                globals()[ "custom" ][ myConcat ] = float( myValue );
                # errors.append( "Problematic Property : '" + str( datProperty ) + "' in 'datsInformation'" );

        # Add all the rest
        if len( dataset[ "yearlyAssessmentInformation" ][ cultivationYearIndex ][ "parcelComparison" ] ) > 0 :
            for parentEntity in dataset[ "yearlyAssessmentInformation" ][ cultivationYearIndex ][ "parcelComparison" ][ 0 ][ parent ] : 
                layer = dataset[ "yearlyAssessmentInformation" ][ cultivationYearIndex ][ "parcelComparison" ][ 0 ][ parent ][ parentEntity ];
                if( isinstance( layer, list ) is False ) : 
                    for property in layer :
                        if parentEntity == "parcelInformation" :
                            myConcat = ( parent + "_" + parentEntity + "_" + property ).lower();
                        else:
                            myConcat = ( parent + "_" + parentEntity + "_" + property ).lower();
                        try :
                            myValue  = layer[ property ];
                            if myValue is not None : 
                                if myValue.isnumeric() : 
                                    globals()[ "custom" ][ myConcat ] = float( myValue );
                                else:
                                    globals()[ "custom" ][ myConcat ] = myValue;
                        except( Exception ) as error :
                            globals()[ "custom" ][ myConcat ] = float( myValue );
                else:

                    for index , item in enumerate( layer ) :
                        if( isinstance( item, dict ) is False ) : 
                            continue;

                        for property in item:
                            myConcat = ( parent + "_" + parentEntity + "_" + property + "_" + str( index ) ).lower();
                            myValue  = item[ property ];

                            try :
                                if myValue.isnumeric() : 
                                    globals()[ "custom" ][ myConcat ] = float( myValue );
                                else:
                                    globals()[ "custom" ][ myConcat ] = myValue;
                            except( Exception ) as error :
                                globals()[ "custom" ][ myConcat ] = myValue;
        else:
            errors.append( "Empty 'parcelComparison' from JSON for year : '" + str( cultivationYear ) + "'" );

        globals()[ "custom" ][ "parcelinformation_cultivationtype" ] = dataset[ "cultivationType" ];

    if len( errors ) > 0 :
        return { "error" : errors };
    else:
        return {
            "crop"        : crop,
            "yearIndex"   : cultivationYearIndex,
            "yearLiteral" : cultivationYear
        }

def evaluateFormula( formula , myFormulaObject ):
    if "C100" in myFormulaObject[ "conversion" ] or "C101" in myFormulaObject[ "conversion" ] or "C102" in myFormulaObject[ "conversion" ] :
        myClass = customFunctions( JSONFileWithUserInput , debug );
        myFormulaObject[ "conversion" ] = myFormulaObject[ "conversion" ].replace( "C100" , str( myClass.getNPK( "C100" ) ) );
        myFormulaObject[ "conversion" ] = myFormulaObject[ "conversion" ].replace( "C101" , str( myClass.getNPK( "C101" ) ) );
        myFormulaObject[ "conversion" ] = myFormulaObject[ "conversion" ].replace( "C102" , str( myClass.getNPK( "C102" ) ) );
        
        if debug is True:
            amTool.logv( "INFO" , amTool.text( "FAIL", "***************  N - P - K  ***************" ) );
            amTool.logv( "INFO" , amTool.text( "HEADER", myFormulaObject[ "original" ] ) );
            amTool.logv( "INFO" , amTool.text( "HEADER", myFormulaObject[ "conversion" ] ) );
            amTool.logv( "INFO" , "" );

    if "cstfn_" in myFormulaObject[ "conversion" ] :
        myClass    = customFunctions( JSONFileWithUserInput , debug );
        myFunction = extract_function_name( myFormulaObject[ "conversion" ] );
        res        = eval( "myClass." + myFunction );
        myFormulaObject[ "conversion" ] = myFormulaObject[ "conversion" ].replace( "cstfn_" , "" );
        myFormulaObject[ "conversion" ] = myFormulaObject[ "conversion" ].replace( myFunction , str( res[ "result" ] ) );

    helper_replaceProcessedToFormula( myFormulaObject );

    # if( str( myFormulaObject[ "description" ] ) == "sust_kpis_dats.environmental_kpis.electricity_consumption" ):
        # print( myFormulaObject[ "conversion" ].replace( "\\" , "" ) );

    try:
        myResult = eval( myFormulaObject[ "conversion" ].replace( "\\" , "" ) );
        myFormulaObject[ "result" ] = str( myResult );
        if debug is True : 
            print( " >>> RESULT <<< : " + str( myFormulaObject[ "result" ] ) + "\r\n" , flush=True );
        return { "res" : myResult };
    except Exception as error : 
        myFormulaObject[ "error" ] = str( error );
        return { "error" : error };

def replace_exact_match( input_string, target, replacement ):
    # Create a regex pattern for the target
    pattern = r'\b' + re.escape( target ) + r'\b'
    
    # Replace the exact match in the input string
    updated_string = re.sub( pattern, replacement, input_string );
    
    return updated_string;

def loadJSONFile( filePath , fileName , type = "json" ):
    myCFG = dict();
    try:
        fileName = filePath + fileName + "." + type;
        if( os.path.exists( fileName ) == False ):
            print("[ amModel Error ] : File [" + fileName + "] Not Found");
            return False;

        f = open( fileName, "r" );
        if f.mode == "r":
            myContents = f.read();
            try:
                if( type == "json" ):
                    myCFG = dict( JSON.loads( myContents ) );
                    print( "File ["+fileName+"] loaded." );
                else:
                    myCFG = myContents;
            except:
                print( "File ["+fileName+"] could not be loaded. Reason : ["+ str(sys.exc_info()[1]) +"]" );
        f.close();
        return myCFG;
    except:
        print( "Unexpected error upon loading Storage ["+fileName+"]:" + str( sys.exc_info()[1] ) );
        return False;

def replace_globals_in_expression(expression, globals_dict):
    global missing_variables;
    """
    Replaces each variable in the expression with its corresponding value from globals_dict.
    Logs any variables that are missing from globals_dict in the missing_variables.

    Parameters:
        expression (str): The expression with variable names to be replaced.
        globals_dict (dict): A dictionary containing variable names as keys and their values.

    Returns:
        str: The expression with variables replaced by their values.
    """

    # Match any variable names in the expression
    variables_in_expression = re.findall( r'\b(?!\d+$)[a-zA-Z_]\w*\b', expression );

    # Replace each variable in the expression with its value from globals_dict
    for var_name in variables_in_expression:
        myDictionary = {};
        if var_name in processedValues : 
            myDictionary = processedValues;

        if var_name in globals_dict : 
            myDictionary = globals_dict;

        if var_name in myDictionary:
            # Get the replacement value from globals_dict
            var_value = myDictionary[ var_name ];
            # Format the replacement as needed
            replacement = f'"{var_value}"' if isinstance( var_value, str ) else str( var_value );
            # Replace in the expression
            expression = re.sub( rf'\b{var_name}\b', replacement, expression );
        else:
            # Track missing variable if it's not in globals_dict
            # If a Variable is not in the Dictionary and is used later in replaces let it as is.
            # Examples are the KNPs that get replaced later and should stay inside the formula , also some Literals of the Crops , etc
            # If a variable is not in the Dictionary but also is not one of those that should stay as is , it should be marked with "0"
            if ( 
                 "cstfn_"   not in var_name 
                 and "IF"   not in var_name 
                 and "C100" not in var_name 
                 and "C101" not in var_name 
                 and "C102" not in var_name 
                 and var_name not in [ 'Mineral','Organic','Apple','Bananas','Barley','Blueberries','Corn','Corn (silage)','Cotton','Grape','Olives','Onion','Potatoes','Rapeseed','Rye','Strawberries','Tomato','Wheat','Wheat (T. aestivum)','Wheat (T. durum)','crop','greenhouse','milk','meat','animal','oyster','honey','grain (silos)' ] 
               ) :
                missing_variables.add( var_name );
                expression = re.sub( rf'\b{var_name}\b', "0", expression );

    # Fix comparisons by replacing "=" with "=="
    expression = expression.replace( "=", "==" );

    def transform_if_recursive( expression ):
        """
        Recursively transforms Excel-style IF statements into Pythonic ternary expressions.
        """
        # Define a regex pattern to match the deepest nested IF first
        pattern = re.compile( r'IF\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\s*\)' );

        while "IF(" in expression:
            expression = re.sub( pattern, lambda match: transform_if( match ), expression );

        return expression;

    def transform_if( match ):
        """
        Transforms a single IF match into a Pythonic ternary expression.
        """
        condition    = match.group( 1 ).strip();
        true_result  = match.group( 2 ).strip();
        false_result = match.group( 3 ).strip();
        
        return f"({true_result} if {condition} else {false_result})";

    # Transform to Pythonic expression
    expression = transform_if_recursive( expression );

    # Report any missing variables
    # if missing_variables:
        # print(f"Warning: The following variables were not found in globals_dict: {missing_variables}")

    return expression

def convertSUMtoPythonCode(input_string):
    """
    Converts Excel-style SUM formulas like SUM(X1:X5) into Pythonic formulas like (X1 + X2 + X3 + X4 + X5).
    
    Args:
        input_string (str): The input string containing the Excel formula.
    
    Returns:
        str: The string with the formula converted to Pythonic style.
    """
    def replace_sum(match):
        # Extract the range, e.g., X1:X5
        range_text = match.group(1)
        # Split into start and end cells, e.g., X1, X5
        start_cell, end_cell = range_text.split(':')
        # Extract the prefix and numbers
        prefix = re.match(r'[A-Za-z]+', start_cell).group(0)
        start_index = int(re.search(r'\d+', start_cell).group(0))
        end_index = int(re.search(r'\d+', end_cell).group(0))
        # Generate the Pythonic formula
        python_formula = f"({'+'.join(f'{prefix}{i}' for i in range(start_index, end_index + 1))})"
        return python_formula

    # Use regex to find all SUM(X1:X5) patterns
    pattern = r'SUM\((\w+\d+:\w+\d+)\)'
    result = re.sub(pattern, replace_sum, input_string)
    
    return result

def extract_function_name( text ):
    # Define the pattern: start with "cstfn_" followed by word characters until a non-word character
    match = re.match( r"^cstfn_[A-Za-z0-9_]+\s*\([^)]+\)", text );
    if match:
        # Return the matched group (the part after "cstfn_")
        return match.group( 0 ).replace( "cstfn_" , "" );
    return None;  # If pattern not found, return None

def save_json_to_file( data, filename ):
    """
    Saves a Python dictionary (or any JSON-serializable object) to a file in JSON format.
    
    Args:
        data (dict): The Python object to be saved as JSON.
        filename (str): The path to the file where the JSON will be saved.
    """
    with open(filename, 'w') as file:
        JSON.dump(data, file, indent=4)  # `indent` makes the output more readable

def helper_printInitialFormula( myFormulaObject ):
    
    try:
        splitString = myFormulaObject[ "description" ].split( "." );
        sheetName   = splitString[ 0 ];
        tableName   = splitString[ 1 ];
        description = "";
        if len( splitString ) == 4:
            description = sheetName + "|" + tableName + "|" + splitString[ 2 ] + "|" + splitString[ 3 ];
        else:
            description = sheetName + "|" + tableName + "|" + splitString[ 2 ];

        print( " >>> INITIAL <<< : " + str( formula[ "formula"] ) , flush=True );
    except Exception as error :
        print( myFormulaObject );
        print( error );

def helper_skipCrazyFunctions( myFormulaObject , myResponse ):
    if "SUMIF" in myFormulaObject[ "original"] : 
        myFormulaObject[ "result" ]     = "None";
        myFormulaObject[ "error" ]      = myFormulaObject[ "original"];
        myFormulaObject[ "conversion" ] = "";
        myResponse.append( myFormulaObject );
        return True;
    elif "ISERR" in myFormulaObject[ "original"] : 
        myFormulaObject[ "result" ]     = "None";
        myFormulaObject[ "error" ]      = myFormulaObject[ "original"];
        myFormulaObject[ "conversion" ] = "";
        myResponse.append( myFormulaObject );
        return True;
    else:
        return False;

def helper_replaceExcelCellsWithFrontEndProperties( myFormulaObject , formula ):
    if debug is False : 
        for target, replacement in sheet_Parcel_With_DATs.items():
            formula[ "formula" ] = replace_exact_match( formula[ "formula" ], target, replacement );
    else:
        with open( "./SteppingHelpers/replacements.txt", 'a' ) as file:
            for target, replacement in sheet_Parcel_With_DATs.items():
                formula[ "formula" ] = replace_exact_match( formula[ "formula" ], target, replacement );

            string = str( myFormulaObject[ "original" ] ) + "\n ==> " + str( formula[ "formula" ] ) + "\n";
            myFormulaObject[ "replace" ] = str( formula[ "formula" ] );
            file.write( string + "\n" );

def helper_replaceProcessedToFormula( myFormulaObject ):
    for target, replacement in processedValues.items():
        myFormulaObject[ "conversion" ] = replace_exact_match( myFormulaObject[ "conversion" ], target, str( replacement ) );

def helper_replaceFrοntEndPropertiesWithFrontEndValues( myFormulaObject , formula ):
    formulas_from_file[ "formulas" ][ index ] = replace_globals_in_expression( formula[ "formula"] , globals()[ "custom" ] )  # Update the formula in the list
    sanitizedFormula = formulas_from_file[ "formulas" ][ index ];
    myFormulaObject[ "conversion" ] = str( sanitizedFormula );
    if debug is True : 
        print( " >>> CONVERTED <<< : " + str( sanitizedFormula ) , flush=True );
        print( " >>> DESCRIPTION <<< : " + str( myFormulaObject[ "description" ] ) , flush=True );
        print( " >>> CELL <<< : " + str( myFormulaObject[ "cell" ] ) , flush=True );
    return sanitizedFormula;

def helper_searchForMissingVariables():
    if missing_variables:
        print(f"Warning: The following variables were not found in globals_dict:");
        for mVar in missing_variables:
            print( mVar );
    for result in myResponse:
        print( "---------------------" );
        if "error" in result: 
            print( JSON.dumps( result , indent=2 ) );
        else:
            print( result[ "result" ] );

def addToProcessedValues( cell , value ):
    global processedValues;
    processedValues[ cell ] = value[ "res" ];

def addToTotalProcessedValues( sheetName , cell , value ):
    global totalProcessedValues;
    # print( str( sheetName ) + " : " + str( cell ) + " : " + str( value[ "res" ] ) );

    mySanitizedSheetName = "";
    if( sheetName   == "Cost-Revenue DATS" ):
        mySanitizedSheetName = "cost_revenue_dats";
    elif( sheetName == "Cost-revenue NO DATS" ):
        mySanitizedSheetName = "cost_revenue_no_dats";
    elif( sheetName == "sust. impact KPIs DATS" ):
        mySanitizedSheetName = "sust_kpis_dats";
    elif( sheetName == "sust. impact KPIs NO DATS" ):
        mySanitizedSheetName = "sust_kpis_no_dats";
    else:
        mySanitizedSheetName = False;

    if mySanitizedSheetName is False:
        return;

    if( mySanitizedSheetName not in totalProcessedValues ):
        totalProcessedValues[ mySanitizedSheetName ] = {};

    if( str( cell ) not in totalProcessedValues[ mySanitizedSheetName ] ):
        totalProcessedValues[ mySanitizedSheetName ][ str( cell ) ] = "";

    totalProcessedValues[ mySanitizedSheetName ][ str( cell ) ] = value[ "res" ];

def resetProcessedValues():
    global processedValues;
    processedValues = {};

def createExport( myResponse , tc_name ):
    myDBObject = {};
    for item in myResponse : 
        # print( item );
        # print(  );
        try:
            splitString = item[ "description" ].split( "." );
            sheetName   = splitString[ 0 ];
            tableName   = splitString[ 1 ];
            description = "";
            if len( splitString ) == 4:
                description = splitString[ 2 ] + "|" + splitString[ 3 ];
            else:
                description = splitString[ 2 ];

            if sheetName not in myDBObject : 
                myDBObject[ sheetName ] = {};

            if tableName not in myDBObject[ sheetName ] : 
                myDBObject[ sheetName ][ tableName ] = {};

            if "error" not in item :
                if item[ "result" ] == "None" : 
                    myDBObject[ sheetName ][ tableName ][ description ] = item[ "error" ];
                else:
                    myDBObject[ sheetName ][ tableName ][ description ] = item[ "result" ];
        except Exception as error :
            print( item );
            print( tc_name );
            print( error );

    save_json_to_file( myDBObject , "./Outputs/export_" + str( tc_name ) + ".json" );
    return myDBObject;

def createMappings( dataSet ):
    myNewObject = {};
    # I hardCode the corresponding ROWS range for each result field in the Excel
    # For example in 'cost_revenue_dats' sheet and 'cost_analysis' table 
    # From column 3 up till and including 38 ihave results. (I set as variable the corresponding column in the Excel)
    # My Input dataSet has an Object { SheetName : { TableName : { FieldName } }
    # Granted that in Python the Objects are always in order created
    # the order of the fields inside the dataSet is the same as the order of the fields in the Excel.
    # i can loop through make the mapping    
    # Goal is to create a mapping between CELL:COLUMN and result from formula.
    # So that i can make aggregations later.
    groups = {
      "cost_revenue_dats" : {
        "cost_analysis"     :  [ 3 , 37 ] , 
        "revenues_analysis" : [ 41 , 47 ]
      },
      "cost_revenue_no_dats" : {
        "cost_analysis"     :  [ 3 , 37 ] , 
        "revenues_analysis" : [ 41 , 47 ]
      }, 
      "sust_kpis_dats" : {
        "economic_productivity_"  : [ 3  , 13 ],
        "economic_efficiency_"    : [ 17 , 19 ],
        "product_quality__"       : [ 24 , 26 ],
        "environmental_kpis"      : [ 30 , 60 ],
        "social_kpis"             : [ 64 , 68 ]
      },
      "sust_kpis_no_dats" : {
        "economic_productivity_"  : [ 3  , 13 ],
        "economic_efficiency_"    : [ 17 , 19 ],
        "product_quality__"       : [ 24 , 26 ],
        "environmental_kpis"      : [ 30 , 60 ],
        "social_kpis"             : [ 64 , 68 ]
      }
    }

    excelColumnForAggregation = "E";

    for sheetName in dataSet : 
        myGroupSettings = groups[ sheetName ];

        if sheetName not in myNewObject:
            myNewObject[ sheetName ] = {};

        for tableName in dataSet[ sheetName ] : 
            if tableName not in myNewObject[ sheetName ]:
                myNewObject[ sheetName ][ tableName ] = {};

            for index , property in enumerate( dataSet[ sheetName ][ tableName ] ) : 
                startingIndex = myGroupSettings[ tableName ][ 0 ] + index;
                endingIndex   = myGroupSettings[ tableName ][ 1 ];
                if( index < endingIndex ) : 
                    myNewProperty = excelColumnForAggregation + str( startingIndex ) + "|" + property;
                    myNewObject[ sheetName ][ tableName ][ myNewProperty ] = dataSet[ sheetName ][ tableName ][ property ];

    if debug is True : 
        print( JSON.dumps( myNewObject , indent=4 ) );
    return myNewObject;

def resolve_formula( formula, dataset ):
    # Regex to match dataset keys in the formula (e.g., sust_kpis_no_dats!E66)
    key_pattern = re.compile( r'([a-zA-Z_]+![A-Z0-9]+)' );
    errors = [];

    def resolve_key( key ):
        # Split the key into dataset name and subkey
        dataset_name, subkey = key.split( '!' );
        # Traverse the dataset to find the value
        if dataset_name in dataset:
            for category, items in dataset[ dataset_name ].items():
                for full_key, value in items.items():
                    if full_key.startswith( subkey ):
                        return str( value );  # Convert value to string
        # print( f"Warning: Key '{key}' not found in dataset." , formula );
        errors.append( f"Warning: Key '{key}' not found in dataset." );
        return "0";  # Default to "0" if key is not found

    # Replace keys in the formula with their resolved values
    def substitute_key( match ):
        key = match.group( 0 );
        return resolve_key( key );

    # Substitute all keys in the formula
    resolved_formula = key_pattern.sub(substitute_key, formula)
    
    if len( errors ) > 0 :
        return { "error" : errors };
    else:
        return resolved_formula;

def create_nested_dict( dot_strings ):
    """
    Converts a list of dot-delimited strings into a nested dictionary.

    Args:
        dot_strings (list): List of strings with dot-delimited keys.

    Returns:
        dict: A nested dictionary representing the parent-child relationships.
    """
    nested_dict = {}

    for dot_string in dot_strings:
        keys = dot_string.split('.')
        current_level = nested_dict

        for key in keys:
            if key not in current_level:
                current_level[key] = {}
            current_level = current_level[key]

    return nested_dict;

def assign_nested_value(dictionary, keys, value):
    """
    Assigns a value to a nested dictionary, creating intermediate dictionaries if necessary.

    Args:
        dictionary (dict): The dictionary to update.
        keys (list): A list of keys representing the path to the value.
        value: The value to assign.

    Example:
        my_dict = {}
        assign_nested_value(my_dict, ["analysis", "social_analysis_", "social_analysis_", "contribution_to_local_employment"], 0.0)
        print(my_dict)
        # Output: {'analysis': {'social_analysis_': {'social_analysis_': {'contribution_to_local_employment': 0.0}}}}
    """
    current_level = dictionary
    for key in keys[:-1]:
        if key not in current_level:
            current_level[key] = {}
        current_level = current_level[key]
    current_level[keys[-1]] = value

def getAnalysis( myMappings ):

    def printResult( item , result = None, resolved_code = None , error = None ):
        if debug is True : 
            print(
              JSON.dumps(
               {
                 "error"   : str( error ),
                 "result"  : str( result ),
                 "formula" : resolved_code,
                 "origin"  : str( item[ "formula" ] ),
                 "sheet"   : str( item[ "sheet" ] ),
                 "desc"    : str( item[ "desc" ] ),
                 "cell"    : str( item[ "cell" ] )
               } , 
               indent = 4
              )
            );

    myDescriptionsList = [];
    for index , item in enumerate( analysis_formulas_from_file[ "formulas" ] ):
        myDescriptionsList.append( item[ "desc" ] );

    myObject = create_nested_dict( myDescriptionsList );
    save_json_to_file( myObject , "./SteppingHelpers/nested_items.json" );

    for index , item in enumerate( analysis_formulas_from_file[ "formulas" ] ):
        try:
            resolved_code = item[ "formula" ];
            if "SUM" in item[ "formula" ] : 
                resolved_code = convertSUMtoPythonCode( item[ "formula" ] );

            resolved_code = resolve_formula( resolved_code , myMappings );
            if "error" in resolved_code:
                printResult( item , None , 0 , resolved_code[ "error" ] );
            else:
                result        = round( eval( resolved_code ) , 2 );
                assign_nested_value( myObject , item[ "desc" ].split( "." ) , result );
                printResult( item , result , resolved_code , None );

        except Exception as error :
            printResult( item , None , None , error );

    save_json_to_file( myObject , "./Outputs/export_analysis_" + str( tc_name ) + ".json" );

def getAnalysis_B():

    def transform_if_recursive( expression ):
        """
        Recursively transforms Excel-style IF statements into Pythonic ternary expressions.
        """
        # Define a regex pattern to match the deepest nested IF first
        pattern = re.compile( r'IF\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\s*\)' );

        while "IF(" in expression:
            expression = re.sub( pattern, lambda match: transform_if( match ), expression );

        return expression;

    def transform_if( match ):
        """
        Transforms a single IF match into a Pythonic ternary expression.
        """
        condition    = match.group( 1 ).strip();
        true_result  = match.group( 2 ).strip();
        false_result = match.group( 3 ).strip();
        
        return f"({true_result} if {condition} else {false_result})";

    def replace_formula_with_values(formula, values_dict):
        # Regular expression to match sheet names and cell references
        pattern = r'([a-zA-Z_]+)!(E\d+)'
        
        def lookup(match):
            sheet, cell = match.groups()
            return str(values_dict.get(sheet, {}).get(cell, '0'))  # Default to '0' if not found

        # Replace matches with corresponding values
        return re.sub(pattern, lookup, formula)

    myResponse = [];

    for index , item in enumerate( analysis_formulas_from_file[ "formulas" ] ):
        formula = item[ "formula" ];
            # Transform to Pythonic expression
        if debug is True:
            amTool.logv( "FAIL" , formula );
        updated_formula = transform_if_recursive( formula );

        # Convert SUM(X1:X10) from Excel to (X1+X2+X3...)
        # updated_formula = convertSUMtoPythonCode( formula );

        updated_formula = replace_formula_with_values( updated_formula, totalProcessedValues );

        try:
            result = eval( updated_formula );
            myResult = {
                 "original"  : formula,
                 "converted" : updated_formula,
                 "result"    : result , 
                 "desc"      : item[ "desc" ],
                 "cell"      : item[ "cell" ],
                 "sheet"     : "analysis_dats_vs._no_dats"
            };

            myResponse.append( myResult );
            amTool.logv( "INFO" , amTool.text( "SUCCESS", "Succesfull Evaluation. [ " + myResult[ "desc" ] + " ] " ) );
            # print( JSON.dumps( myResult , indent = 4 ) );
        except( Exception ) as error :
            if debug is True:
                amTool.logv( "INFO" , amTool.text( "FAIL", "FAILURE to EVAL Aanalysis Formula" ) );
                amTool.logv( "INFO" , formula );
                amTool.logv( "INFO" , "" );

    return myResponse;

def select_tc_name():
    input_dir = "./InputTCs";
    try:
        entries = os.listdir( input_dir );
    except Exception as error:
        print( "[ amModel Error ] : Unable to read InputTCs folder" );
        print( error );
        sys.exit( 1 );

    json_files = sorted(
        [ f for f in entries if f.lower().endswith( ".json" ) ]
    );

    if len( json_files ) == 0:
        print( "[ amModel Error ] : No JSON files found in InputTCs" );
        sys.exit( 1 );

    print( "\nAvailable datasets in InputTCs:" );
    for index, filename in enumerate( json_files, start = 1 ):
        print( f"  {index}. {filename}" );

    while True:
        selection = input( "Select dataset by number or name: " ).strip();
        if selection.isdigit():
            selection_index = int( selection ) - 1;
            if 0 <= selection_index < len( json_files ):
                return os.path.splitext( json_files[ selection_index ] )[ 0 ];
        else:
            candidate = selection;
            if not candidate.lower().endswith( ".json" ):
                candidate = candidate + ".json";
            for filename in json_files:
                if filename.lower() == candidate.lower():
                    return os.path.splitext( filename )[ 0 ];

        print( "Invalid selection. Try again." );

def select_cultivationYear( tc_name ):
    input_dir = "./InputTCs";
    myJSON = amTool.load( input_dir + "/" , tc_name , "json" );
    cultivationPeriods = [];

    print( "\nAvailable Cultivation Periods:" );
    for index, period in enumerate( myJSON[ "yearlyAssessmentInformation" ] , start = 1 ):
        cultivationPeriods.append( period[ "cultivationYear" ] );
        print( f"  {index}. Year: {str( period[ "cultivationYear" ] )}" );

    while True:
        selection = input( "Select cultivation Period: " ).strip();
        if selection.isdigit():
            selection_index = int( selection ) - 1;
            if 0 <= selection_index < len( myJSON[ "yearlyAssessmentInformation" ] ):
                return cultivationPeriods[ selection_index ];

        print( "Invalid selection. Try again." );

clearAllLogs();

tc_name         = args.tc_name if args.tc_name else select_tc_name();
cultivationYear = args.cultivationYear if args.cultivationYear else select_cultivationYear( tc_name );

# File from Ivaylos Export. These are the user provided Values frομ the Form Fields on the Front End.
JSONFileWithUserInput       = loadJSONFile( filePath = "./InputTCs/" ,          fileName = tc_name ,        type = "json" );

# Load the JSON Input and create globals() with nested onomatology. 
# Eg. "parcelassessmentwithdats_marketinformation_waterprice"
# NOTE : Arrays are excluded. Only Objects are added to Globals.
try :
    output = createMemoryObject( JSONFileWithUserInput , cultivationYear );
    if "error" in output:
        print( JSON.dumps({ "error" : output[ "error" ] }), file=sys.stderr );
        sys.exit( 1 );

    JSONFileWithUserInput[ "crop" ]      = output[ "crop" ];
    JSONFileWithUserInput[ "yearIndex" ] = output[ "yearIndex" ];

    # Ivaylos JSON does does not have the same Properties as the Excel. There are some naming differences making it really hard to 
    # find which property from the JSON maps to which property on the Excel of Polimi. 
    # So Jack and I created a Mapping. Which consists of the JSON Properties (with a concatenated object like name) and the corresponding Cell in the excel.
    # So i end up with a JSON that has mappings like  '{ "A1" : "water_amount" , "A2" : "price_of_water" }'
    # That way i have a Mapping from "Ivaylos Front End Property" -> "Mapping in JSON" -> "Actual excel Columh:Cell"
    # Now when i excute a formula like "(A2 + A3)" found in the excel 
    # i can find through mappings that the A2 is for example "water_amount" and A3 is "price_of_water" and Convert it to "(water_amount + price_of_water)" 
    sheet_Parcel_With_DATs      = loadJSONFile( filePath = "./SteppingHelpers/" ,   fileName = "mappings" ,   type = "json" );

    # This is a JSON derived from all the Formulas of the Excel.
    # VB Script is being used to export the Formulas into seperate files per sheet.
    # Then a Script "convert_formulas_to_json.py" is used to create this JSON.
    formulas_from_file          = loadJSONFile( filePath = "./ConvertedFormulas/" , fileName = "ALL_toJSON" , type = "json" );

    # This is a JSON that has all the Analysis Formulas. Those Formulas are from the "Analysis DATS vs. NO DATS" sheet.
    # It is manually created by using the VB Script to export the formulas. 
    # Then a Script "convert_formulas_to_json.py" is used to create this JSON.
    analysis_formulas_from_file = loadJSONFile( filePath = "./ConvertedFormulas/" , fileName = "Analytics_toJSON" , type = "json" );

    if debug_Globals is True : 
        printGlobals();

    myResponse   = [];
    myErrors     = [];
    currentSheet = "";

    if loop   == True :
        # Save the result in the following file
        with open( "./SteppingHelpers/exported_formulas.txt", "w" ) as file:
            for index, formula in enumerate( formulas_from_file[ "formulas" ] ):
                
                # ProcessedValues holds the results of calculation on specific sheet. 
                # It is used for self reference formulas. Where a formula requires a value 
                # from a field that has previously been processed. So all processes store the outcome here.
                # There is no need for this to move to the next Sheet , references are only on the same Sheet at this excel.
                if( currentSheet != str( formula[ "sheet" ] ) ):
                    currentSheet = str( formula[ "sheet" ] );
                    resetProcessedValues();

                myFormulaObject = {};
                myFormulaObject[ "original" ]    = str( formula[ "formula" ] );
                myFormulaObject[ "description" ] = str( formula[ "desc" ] );
                myFormulaObject[ "sheet" ]       = str( formula[ "sheet" ] );
                myFormulaObject[ "cell" ]        = str( formula[ "cell" ] );

                if debug is True : 
                    helper_printInitialFormula( myFormulaObject );

                if formula[ "formula" ] == "":
                    continue;

                # Skip Formulas that i have not coded an implementation for the function they are using.
                # Those are generally an issue and should be solved even though they are 1-2 or two in total.
                if helper_skipCrazyFunctions( myFormulaObject , myResponse ) is True : 
                    continue;

                # Convert SUM(X1:X10) from Excel to (X1+X2+X3...)
                formula[ "formula" ] = convertSUMtoPythonCode( formula[ "formula" ] );

                # Replace the excel Cells in the Formula with Ivaylos Properties
                # Example : G250/G10 
                #           ==> parcelassessmentwithdats_outputinformation_cropproduction / parcelinformation_parceldimension
                helper_replaceExcelCellsWithFrontEndProperties( myFormulaObject , formula );

                # Replace Ivaylos properties with the actual values.
                # Example : parcelassessmentwithdats_outputinformation_cropproduction / parcelinformation_parceldimension
                #           ==> 291.1 / 4
                finalFormula = helper_replaceFrοntEndPropertiesWithFrontEndValues( myFormulaObject , formula );

                # Evaluate the formula 
                # Successful Evaluation : It is a simple formula and we are ok
                # Failed Evaluation : It either has 
                # 1) Custom functions inside it that are wrong 
                # 2) The Fixed Cells from KNP values are wrong
                # 3) There are missing Properties/Values/Mappings.
                myFormulaResult = evaluateFormula( finalFormula , myFormulaObject );

                if "error" not in myFormulaResult:
                    # These keep the name of the Sheet inside them and do not reset on every sheet.
                    # Meaning at the end they have all results from every single processed value
                    addToTotalProcessedValues( formula[ "sheet" ] , str( formula[ "cell" ] ) , myFormulaResult );
                    
                    # These reset on every change of the Sheet. They are used only for self-reference.
                    # Yes i should have only the above Object , but the above Object was created at a 
                    # later stage and refactoring everything to use it instead of this one was never done.
                    addToProcessedValues( str( formula[ "cell" ] ) , myFormulaResult );
                else:
                    # print( JSON.dumps( processedValues , indent=4 ) );
                    if debug is True : 
                        print();
                        # print(  "------------------ PROBLEMATIC FORMULA ---------------------"  );
                        # print( JSON.dumps( myFormulaObject , indent=4 ) );

                file.write( finalFormula + "\n" );
                myResponse.append( myFormulaObject );
                if( "error" in myFormulaObject ):
                    myErrors.append( myFormulaObject );

            # if debug_missingVariables is True : 
                # helper_searchForMissingVariables();

    # Save the in-memory Object with the results in a JSON file for easier debugging.
    save_json_to_file( myResponse , "./SteppingHelpers/FormulaResults.json" );

    # Create the Export JSON for Ivaylo
    dataSet = createExport( myResponse , tc_name );

    if( loop_analytics == True ):
        myResponse = getAnalysis_B();
        save_json_to_file( myResponse , "./Outputs/export_analysis_" + str( tc_name ) + ".json" );

except Exception as error :
    print( JSON.dumps({ "error" : "Improper JSON" }), file=sys.stderr );
    sys.exit( 1 );


