import re;
import os;
import sys;
import json as JSON;

def loadTextFile( filePath , fileName , type = "txt" ):
    try:
        fileName = filePath + fileName + "." + type;
        if( os.path.exists( fileName ) == False ):
            print("[ amModel Error ] : File [" + fileName + "] Not Found");
            return False;

        f = open( fileName, "r" );
        if f.mode == "r":
            try:
                myContents = f.read();
                f.close();
                return myContents;
            except:
                print( "File ["+fileName+"] could not be loaded. Reason : ["+ str(sys.exc_info()[1]) +"]" );
    except:
        print( "Unexpected error upon loading Storage ["+fileName+"]:" + str( sys.exc_info()[1] ) );
        return False;

def remove_e_number_pattern(input_string):
    """
    Removes occurrences of '$E$NUMBER:' from the input string.
    
    Args:
        input_string (str): The input string containing the patterns.
    
    Returns:
        str: The modified string with patterns removed.
    """
    # Pattern to match "$E$NUMBER:"
    pattern = r"\$E\$\d+: =\s*?"
    # Replace matches with an empty string
    result = re.sub(pattern, '', input_string)

    pattern = r"\$F\$\d+: =\s*?"
    # Replace matches with an empty string
    result = re.sub(pattern, '', result)
    return result

def replace_KNP(input_string, replacements):
    """
    Replaces every occurrence of 'C' followed by a number (e.g., C81, C82)
    in the input string with the corresponding 'value' from the dictionary.

    Args:
        input_string (str): The input string containing 'C' + 'NUMBER' patterns.
        replacements (dict): A dictionary where keys are 'C' + 'NUMBER' and
                             values are dictionaries with 'name' and 'value'.

    Returns:
        str: The modified string with patterns replaced by the 'value' from the dictionary.
    """
    # Pattern to match "C" followed by digits
    pattern = r'C\d+'

    def replace_match(match):
        key = match.group(0)  # Extract the matched text (e.g., "C81")
        if key in replacements:
            return str(replacements[key]['value'])  # Replace with the 'value' field
        return key  # If not found, keep the original text

    # Replace all occurrences of the pattern
    result = re.sub(pattern, replace_match, input_string)
    return result

def save_json_to_file(data, filename):
    """
    Saves a Python dictionary (or any JSON-serializable object) to a file in JSON format.
    
    Args:
        data (dict): The Python object to be saved as JSON.
        filename (str): The path to the file where the JSON will be saved.
    """
    with open(filename, 'w') as file:
        JSON.dump(data, file, indent=4)  # `indent` makes the output more readable

emissions = {
    "C79" : { "name" : "EF1"                        , "value" :	0.01 } , 
    "C80" : { "name" : "EF1 SW"                     , "value" :	0.016 } , 
    "C81" : { "name" : "EF1 OW"                     , "value" :	0.006 } , 
    "C82" : { "name" : "EF1 AD"                     , "value" :	0.006 } , 
    "C84" : { "name" : "EF4"                        , "value" :	0.01 } , 
    "C85" : { "name" : "EF4 W"                      , "value" :	0.014 } , 
    "C86" : { "name" : "EF4 D"                      , "value" :	0.005 } , 
    "C87" : { "name" : "Frac GASF"                  , "value" :	0.11 } , 
    "C88" : { "name" : "Frac GASM"                  , "value" :	0.21 } , 
    "C89" : { "name" : "FracLEACH"                  , "value" :	0.24 } , 
    "C90" : { "name" : "FracLEACH D"                , "value" :	0 } , 
    "C91" : { "name" : "EF5"                        , "value" :	0.011 } , 
    "C92" : { "name" : "CF1"                        , "value" :	1.571428571 } , 
    "C93" : { "name" : "GWP-N2O"                    , "value" :	273 } , 
    "C94" : { "name" : "Lower Heating Value Diesel" , "value" : 35.9 } , 
    "C95" : { "name" : "EF diesel agri"             , "value" : 0.0741 } 
}


configuration = [
    {
      "fileName" : "sust. impact KPIs DATS" , 
      "functions" : [ "remove_e_number_pattern( myFile )" , "replace_KNP( myFile , emissions )" ] , 
      "replacements" : [
          ( "$" , "" ),
          ( "'General Information'!" , "" ),
          ( "'Parcel 1 with DATSs'!" , "" ),
          ( "'sust. impact KPIs DATS'!" , "" )
      ],
      "fn_replacements" : {
          "(G186+G188+G190)" : "cstfn_calculate_dynamic_k( )" , 
          "(G186+G188+G190)" : "cstfn_calculate_dynamic_l( )" , 
          "(G101*G102*(G103/100))+(G108*G109*(G110/100))+(G115*G116*(G117/100))+(G122*G123*(G124/100))+(G129*G130*(G131/100))+(G136*G137*(G138/100))+(G143*G144*(G145/100))+(G150*G151*(G152/100))+(G157*G158*(G159/100))+(G164*G165*(G166/100))" : "cstfn_calculate_dynamic_o( )" ,
          "(G101*G102*(G104/100))+(G108*G109*(G111/100))+(G115*G116*(G118/100))+(G122*G123*(G125/100))+(G129*G130*(G132/100))+(G136*G137*(G139/100))+(G143*G144*(G146/100))+(G150*G151*(G153/100))+(G157*G158*(G160/100))+(G164*G165*(G167/100))" : "cstfn_calculate_dynamic_n( )" , 
          "(G101*G102*(G105/100))+(G108*G109*(G112/100))+(G115*G116*(G119/100))+(G122*G123*(G126/100))+(G129*G130*(G133/100))+(G136*G137*(G140/100))+(G143*G144*(G147/100))+(G150*G151*(G154/100))+(G157*G158*(G161/100))+(G164*G165*(G168/100))" : "cstfn_calculate_dynamic_m( )" , 
      }
    },
    {
      "fileName" : "sust. impact KPIs NO DATS" , 
      "functions" : [ "remove_e_number_pattern( myFile )" , "replace_KNP( myFile , emissions )" ] , 
      "replacements" : [
          ( "$" , "" ),
          ( "'General Information'!" , "" ),
          ( "'Parcel 1 without DATSs'!" , "" ),
          ( "'sust. impact KPIs NO DATS'!" , "" ),
          ( "'sust. impact KPIs DATS'!", "" )
      ],
      "fn_replacements" : {
          "(H101*H102*(H103/100))+(H108*H109*(H110/100))+(H115*H116*(H117/100))+(H122*H123*(H124/100))+(H129*H130*(H131/100))+(H136*H137*(H138/100))+(H143*H144*(H145/100))+(H150*H151*(H152/100))+(H157*H158*(H159/100))+(H164*H165*(H166/100))" : "cstfn_calculate_dynamic_p( )" , 
          "(H101*H102*(H104/100))+(H108*H109*(H111/100))+(H115*H116*(H118/100))+(H122*H123*(H125/100))+(H129*H130*(H132/100))+(H136*H137*(H139/100))+(H143*H144*(H146/100))+(H150*H151*(H153/100))+(H157*H158*(H160/100))+(H164*H165*(H167/100))" : "cstfn_calculate_dynamic_q( )" , 
          "(H101*H102*(H105/100))+(H108*H109*(H112/100))+(H115*H116*(H119/100))+(H122*H123*(H126/100))+(H129*H130*(H133/100))+(H136*H137*(H140/100))+(H143*H144*(H147/100))+(H150*H151*(H154/100))+(H157*H158*(H161/100))+(H164*H165*(H168/100))" : "cstfn_calculate_dynamic_r( )" , 
          "(H67*H68)+(H70*H71)+(H73*H74)+(H76*H77)+(H79*H80)+(H82*H83)+(H85*H86)+(H88*H89)+(H91*H92)+(H94*H95)" : "cstfn_calculate_dynamic_s( )" , 
          "(H186+H188+H190)"     : "cstfn_calculate_dynamic_t( )" , 
          "(H186+H188+H190)"     : "cstfn_calculate_dynamic_u( )" , 
          "(H186+H188+H190)/E20" : "cstfn_calculate_dynamic_v( )" , 
          "(H186+H188+H190)/E19" : "cstfn_calculate_dynamic_w( )" 
      }
    },
    {
      "fileName" : "Cost-Revenue DATS" , 
      "functions" : [ "remove_e_number_pattern( myFile )" ] , 
      "replacements" : [
          ( "$" , "" ),
          ( "'Parcel 1 with DATSs'!" , "" ),
          ( "'General Information'!" , "" )
      ],
      "fn_replacements" : {
          # "((K54*G42)+(K56*G43)+(K58*G44))/K10"           : "cstfn_calculate_dynamic( )",
          "((D23+D24)+(I23+I24)+(M23+M24))": "cstfn_calculate_dynamic_x( )",
          "(G67*G68*D43)+(G70*G71*D44)+(G73*G74*D45)+(G76*G77*D46)+(G79*G80*D47)+(G82*G83*D48)+(G85*G86*D49)+(G88*G89*D50)+(G91*G92*D51)+(G94*G95*D52)"     : "cstfn_calculate_dynamic_b( )",
          "(G101*G102*D54)+(G108*G109*D55)+(G115*G116*D56)+(G122*G123*D57)+(G129*G130*D58)+(G136*G137*D59)+(G143*G144*D60)+(G150*G151*D61)+(G157*G158*D62)+(G164*G165*D63)" : "cstfn_calculate_dynamic_c( )",
          "((D65*G173)+(D66*G175)+(D69*G177))" : "cstfn_calculate_dynamic_d( )",
          "((D71*G186)+(D72*G188)+(D73*G190))" : "cstfn_calculate_dynamic_e( )"
      }
    },
    {
      "fileName" : "Cost-revenue NO DATS" , 
      "functions" : [ "remove_e_number_pattern( myFile )" ] , 
      "replacements" : [
          ( "$" , "" ),
          ( "'Parcel 1 without DATSs'!" , "" ),
          ( "'General Information'!" , "" )
      ],
      "fn_replacements" : {
          # "((L48*G99)+(L50*G100)+(L52*G101))/L10" : "cstfn_calculate_dynamic_f( )",
          "(H67*H68*H43)+(H70*H71*H44)+(H73*H74*H45)+(H76*H77*H46)+(H79*H80*H47)+(H82*H83*H48)+(H85*H86*H49)+(H88*H89*H50)+(H91*H92*H51)+(H94*H95*H52)"     : "cstfn_calculate_dynamic_g( )",
          "(H101*H102*I54)+(H108*H109*I55)+(H115*H116*I56)+(H122*H123*I57)+(H129*H130*I58)+(H136*H137*I59)+(H143*H144*I60)+(H150*H151*I61)+(H157*H158*I62)+(H164*H165*I63)" : "cstfn_calculate_dynamic_h( )",
          # "(H101*H102*I54)+(H108*H109*I55)+(H115*H116*I56)+(H122*H123*I57)+(H129*H130*I58)+(H136*H137*I59)+(H143*H144*I60)+(H150*H151*I61)+(H157*H158*I62)+(H164*H165*I63)" : "cstfn_calculate_dynamic_i( )",
          # "(H71*H186+H72*H188+H73*H190)" : "cstfn_calculate_dynamic_j( )"
      }
    },
    {
      "fileName" : "Analysis DATS vs. NO DATS" , 
      "functions" : [ "remove_e_number_pattern( myFile )" ] , 
      "replacements" : [
          ( "$" , "" ),
          ( "'Cost-revenue DATS'"         , "cost_revenue_dats" ),
          ( "'Cost-revenue NO DATS'"      , "cost_revenue_no_dats" ),
          ( "'sust. impact KPIs DATS'"    , "sust_kpis_dats" ),
          ( "'sust. impact KPIs NO DATS'" , "sust_kpis_no_dats" ),
          ( "'General Information'!" , "" )
      ],
      "fn_replacements" : {
      }
    }
]

myJSON      = { "formulas": [] }
myAnalytics = { "formulas": [] }

for index , cfg in enumerate( configuration ): 
    try:
        myFile = loadTextFile( "./ExcelFormulaOutputs/" , cfg[ "fileName" ] , type = "txt" );
        if myFile is False : 
            continue;

        if cfg[ "fileName" ] == "Analysis DATS vs. NO DATS" :
            continue;

        for fn in cfg[ "functions" ] : 
            myFile = eval( fn );

        for replacement in cfg[ "replacements" ] : 
            myFile = myFile.replace( replacement[ 0 ] , replacement[ 1 ] );

        for fn in cfg[ "fn_replacements" ] :
            myFile = myFile.replace( fn , cfg[ "fn_replacements" ][ fn ] );

        for line in myFile.splitlines():
            if line == "":
                continue;

            myPair    = line.lstrip().split( " | " );
            myFormula = myPair[ 0 ];
            myDesc    = myPair[ 1 ].replace( "," , "" ).replace( "." , "" ).replace( "_" , "." ).rstrip().replace( " " , "_" ).replace( "(" , "" ).replace( ")" , "" ).lower();
            myCell    = myPair[ 2 ];

            myTempJSON = { 
                "parent":"" , 
                "desc" : myDesc , 
                "sheet" : cfg[ "fileName" ] , 
                "formula" : myFormula , 
                "cell"    : myCell
            };

            myJSON[ "formulas" ].append( myTempJSON );
    except Exception as error : 
        print( "Normal" );
        print( error );

save_json_to_file(myJSON, "./ConvertedFormulas/ALL_toJSON.json" );

for index , cfg in enumerate( configuration ): 
    try:
        myFile = loadTextFile( "./ExcelFormulaOutputs/" , cfg[ "fileName" ] , type = "txt" );
        if myFile is False : 
            continue;

        if cfg[ "fileName" ] != "Analysis DATS vs. NO DATS" :
            continue;

        for fn in cfg[ "functions" ] : 
            myFile = eval( fn );

        for replacement in cfg[ "replacements" ] : 
            myFile = myFile.replace( replacement[ 0 ] , replacement[ 1 ] );

        for fn in cfg[ "fn_replacements" ] :
            myFile = myFile.replace( fn , cfg[ "fn_replacements" ][ fn ] );

        for line in myFile.splitlines():
            if line == "":
                continue;

            myPair = line.lstrip().split( " | " );
            myFormula = myPair[ 0 ];
            myDesc    = myPair[ 1 ].replace( "," , "" ).replace( "." , "" ).replace( "_" , "." ).rstrip().replace( " " , "_" ).replace( "(" , "" ).replace( ")" , "" ).lower();
            myCell    = myPair[ 2 ];
            
            # if( myCell == "E76" ):
                # print( line );

            myTempJSON = { 
                "parent":"" , 
                "desc" : myDesc , 
                "sheet" : cfg[ "fileName" ] , 
                "formula" : myFormula , 
                "cell"    : myCell
            };

            myAnalytics[ "formulas" ].append( myTempJSON );
    except Exception as error : 
        print( "Analytics" );
        print( error );

save_json_to_file(myAnalytics, "./ConvertedFormulas/Analytics_toJSON.json" );
