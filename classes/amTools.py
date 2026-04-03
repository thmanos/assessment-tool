import os;
import datetime;
import sys;
import json as JSON;
from time import time;

class amTools:
 def __init__( self ):
  """Class for Misc Tools"""
  self.bcolors = { 
      "HEADER"  : "\033[95m",
      "BLUE"    : "\033[94m",
      "INFO"    : "\033[96m",
      "SUCCESS" : "\033[92m",
      "WARNING" : "\033[91m",
      "FAIL"    : "\033[93m",
      "ENDC"    : "\033[0m"
  }
  # self.log( "Tools Initiated" );

 def text( self , color , text ):
     return self.bcolors[ color ] + str( text ) + self.bcolors[ "ENDC" ];

 def log( self , myString , object = None , debug = True  , frameinfo = None ):
     if debug == True : 
         if frameinfo is not None :
             myLine = "[ Line : " + str( frameinfo.lineno ) + " ] ";
         else :
             myLine = "";

         myCurrentTime = datetime.datetime.now();
         myTimePrefix = "[" + datetime.datetime.strftime( myCurrentTime , "%Y-%m-%d %H:%M:%S" ) + "]  : ";
         print( 
           self.bcolors[ "INFO" ] + 
           "[" + 
           datetime.datetime.strftime( myCurrentTime , "%Y-%m-%d %H:%M:%S" ) + 
           "] " + 
           self.bcolors[ "ENDC" ] + 
           ": " + myLine + " " + str( myString ) , 
           flush = True
         );
         if object is not None :
             print( self.bcolors[ "WARNING" ] + myTimePrefix + " ---- Object ---- " + self.bcolors[ "ENDC" ] , flush = True );
             try:
                 isJSON = JSON.loads( object );
                 print( JSON.dumps( object, indent = 4 ) , flush = True );
             except( Exception ) as error:
                 print( object , flush = True );
             print( self.bcolors[ "WARNING" ] + myTimePrefix + " ---- End ---- " + self.bcolors[ "ENDC" ] , flush = True );
             print( ""  , flush = True );

 def logv( self , color = "HEADER" , text = "" , object = None , debug = True  , frameinfo = None ):
     if debug == True : 
         if frameinfo is not None :
             myLine = "[ Line : " + str( frameinfo.lineno ) + " ] ";
         else :
             myLine = "";

         myCurrentTime = datetime.datetime.now();
         myTimePrefix = "[" + datetime.datetime.strftime( myCurrentTime , "%Y-%m-%d %H:%M:%S" ) + "]  : ";
         print( 
             self.bcolors[ color ] + 
                 "[" + datetime.datetime.strftime( myCurrentTime , "%Y-%m-%d %H:%M:%S" ) + "] " + 
             self.bcolors[ "ENDC" ] + ": " + 
                 myLine + " " + str( text ) , 
                 flush = True
         );

         if object is not None :
             print( self.bcolors[ color ] + myTimePrefix + " ---- Object ---- " + self.bcolors[ "ENDC" ] , flush = True );
             if isinstance(object, dict):
                 print( JSON.dumps( object, indent = 4 ) , flush = True );
             else:
                 try:
                     isJSON = JSON.loads( object );
                     print( JSON.dumps( object, indent = 4 ) , flush = True );
                 except( Exception ) as error:
                     print( object , flush = True );
             print( self.bcolors[ color ] + myTimePrefix + " ---- End ---- " + self.bcolors[ "ENDC" ] , flush = True );
             print( ""  , flush = True );

 def load( self , filePath , fileName , type = "json" ):
     """
      Loads Configuration from Disk
     """
     myCFG = dict();
     try:
         fileName = filePath + fileName + "." + type;
         if( os.path.exists( fileName ) == False ):
            self.log("[ amModel Error ] : File [" + fileName + "] Not Found");
            return False;

         f = open( fileName, "r" );
         if f.mode == "r":
             myContents = f.read();
             try:
                 if( type == "json" ):
                     myCFG = JSON.loads( myContents );
                     self.log( "File ["+fileName+"] loaded." );
                 else:
                     myCFG = myContents;
             except:
                 self.log( "File ["+fileName+"] could not be loaded. Reason : ["+ str(sys.exc_info()[1]) +"]" );
         f.close();
         return myCFG;
     except:
         self.log( "Unexpected error upon loading Storage ["+fileName+"]:" + str( sys.exc_info()[1] ) );
         return False;

 def logFile( self , myString ) : 
     myCurrentTime = datetime.datetime.now();
     myPrefix = "[" + datetime.datetime.strftime( myCurrentTime , "%Y-%m-%d %H:%M:%S" ) + "] : ";

     fd = open( "./log.log" , "a+");
     fd.write( myPrefix + str( myString ) + "\n");
     fd.close();

 def log_curl( self , method , postData , endpoint , file=False , auth=False ):
     myMethod      = "";
     myAuth        = "";
     myContentType = "Content-type: application/json";
     myEndpoint    = endpoint;

     if( method     == "post" ):   myMethod = "-XPOST";
     elif( method   == "get" ):    myMethod = "-XGET";
     elif( method   == "delete" ): myMethod = "-XDELETE";
     elif( method   == "put" ):    myMethod = "-XPUT";
     else: myMethod =  "XGET";

     if( auth is not False ): myAuth = auth;

     if( file == False ):
         myPostData  = JSON.dumps( postData ).replace( "'", "\\\"" ).replace( "\"", "\\\"" );
         myLogString = f"curl {myMethod} -u {myAuth} -H \"{myContentType}\" -d \"{myPostData}\" \"{myEndpoint}\" ";
     else:
         myFileName  = file["name"];
         myFilePath  = file["path"];
         myLogString = f"curl -u {myAuth} -F name=\"{myFileName}\" -F filedata=@{myFilePath}\" \"{myEndpoint}\" ";

     print();
     print( " [ CURL ] " )
     print( myLogString );
     print();
     return myLogString;

 def getUID( self , hash ):
     currentDate     = datetime.datetime.now();
     currentTS       = round( currentDate.timestamp() );
     myStringHash    = str( currentTS ) + str( hash );
     
     return myStringHash;

 def isValidJSON( self , json ):
     try:
         myJSON = JSON.loads( json );
     except ValueError as error :
         return False;
     return True;

 def isInt( self , value ):
     try:
         isValueInt = int( value );
         return True;
     except( Exception ) as error:
         return False;
