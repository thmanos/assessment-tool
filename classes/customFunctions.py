import json as JSON;
from classes.amTools import amTools;

class customFunctions:
    def __init__( self , UserInputs , debug = False):
       """Class for Functions Tools"""
       # self.UserInputs = JSON.loads( JSON.dumps( UserInputs ).lower() );
       self.UserInputs      = UserInputs;
       self.cultivationType = UserInputs[ "cultivationType" ];
       self.crop            = UserInputs[ "crop" ];
       self.yearIndex       = UserInputs[ "yearIndex" ];
       self.amTool = amTools();
       self.debug = debug;
    
    def printAlert( self , line ):
        if self.debug is True:
            self.amTool.logv( "INFO" , self.amTool.text( "FAIL", "--------------------- CUSTOM FUNCTIONS ----------------------" ) );
            self.amTool.logv( "INFO" , self.amTool.text( "FAIL", "-------------------- customFunctions.py ---------------------" ) );
            self.amTool.logv( "INFO" , self.amTool.text( "FAIL", "------------------------ Line:" + str( line ) + " ---------------------------" ) );
            self.amTool.logv( "INFO" , self.amTool.text( "FAIL", "------------------------- FORMULA ---------------------------" ) );

    def getNPK( self , cell ):
        cellMap = {
          "C100" : "N" , 
          "C101" : "P" , 
          "C102" : "K"
        }

        myNPK = {
            "Apple"               : { "N" : 0.0007  , "P" : 0.00022 , "K" : 0.0018  },
            "Bananas"             : { "N" : 0.00166 , "P" : 0.00036 , "K" : 0.0043  },
            "Barley"              : { "N" : 0.02    , "P" : 0.0083  , "K" : 0.0066  },
            "Blueberries"         : { "N" : 0.0047  , "P" : 0.0011  , "K" : 0.0048  },
            "Corn"                : { "N" : 0.0147  , "P" : 0.0065  , "K" : 0.0042  },
            "Corn (silage)"       : { "N" : 0.0043  , "P" : 0.0014  , "K" : 0.0033  },
            "Cotton"              : { "N" : 0.065   , "P" : 0.029   , "K" : 0.039   },
            "Grape"               : { "N" : 0.00132 , "P" : 0.00025 , "K" : 0.00224 },
            "Olives"              : { "N" : 0.00287 , "P" : 0.00049 , "K" : 0.00442 },
            "Onion"               : { "N" : 0.003   , "P" : 0.0012  , "K" : 0.004   },
            "Potatoes"            : { "N" : 0.0035  , "P" : 0.0013  , "K" : 0.0058  },
            "Rapeseed"            : { "N" : 0.031   , "P" : 0.02    , "K" : 0.021   },
            "Rye"                 : { "N" : 0.025   , "P" : 0.0082  , "K" : 0.0055  },
            "Strawberries"        : { "N" : 0.0058  , "P" : 0.0011  , "K" : 0.0081  },
            "Tomato"              : { "N" : 0.0032  , "P" : 0.001   , "K" : 0.0068  },
            "Wheat"               : { "N" : 0.0202  , "P" : 0.0082  , "K" : 0.0052  },
            "Wheat (T. aestivum)" : { "N" : 0.0202  , "P" : 0.0082  , "K" : 0.0052  },
            "Wheat (T. durum)"    : { "N" : 0.0203  , "P" : 0.0084  , "K" : 0.0051  }
        }

        if self.crop in myNPK : 
            return myNPK[ self.crop ][ cellMap[ cell ] ];
        else:
            return False;

    def getNO2Emissions( self ):
        # this is obsolete the replace takes place in convert_formulas_to_json.py inside the emissions object
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

    def calculate_cost( self , pesticidesUsageInformation, fuelForTemperatureControlInformation ):
        # Ensure both lists have the same length by iterating over the minimum length
        min_length = min(len(pesticidesUsageInformation), len(fuelForTemperatureControlInformation))

        total_cost = 0

        # Loop over each corresponding pair of elements
        for i in range(min_length):
            # Extract pesticide info
            pesticide            = pesticidesUsageInformation[i]
            number_of_treatments = pesticide['numberOfTreatments']
            average_quantity     = pesticide['averageQuantity']

            # Extract fuel info
            fuel          = fuelForTemperatureControlInformation[i]
            fuel_quantity = fuel['quantity']

            # Calculate the term for the current pair and add it to the total cost
            term        = (number_of_treatments * average_quantity) + fuel_quantity
            total_cost += term

        return total_cost;

    def calculate_dynamic( self ):   # "((K54*G42)+(K56*G43)+(K58*G44))/K10"
        myArray = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "fuelForTemperatureControlInformation" ];
        myparcelDimensions = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "parcelInformation" ][ "parcelDimension" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] + item[ "productPrice" ];

        return { 
          "result"     : myTotal / myparcelDimensions , 
          "expression" : "((K54*G42)+(K56*G43)+(K58*G44))/K10" 
        }

    def calculate_dynamic_b( self ): # "(K82*K83*G50)+(K85*K86*G51)+(K88*K89*G59)"
        myArray = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "pesticidesUsageInformation" ];

        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "(K82*K83*G50)+(K85*K86*G51)+(K88*K89*G59)"
        }

    def calculate_dynamic_c( self ): # "(K95*K96*G68)+(K102*K103*G69)+(K109*K110*G70)"
        myArray = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "fertilizersUsageInformation" ];

        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * 1000 * item[ "averageQuantity" ] * item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "(K95*K96*G68)+(K102*K103*G69)+(K109*K110*G70)"
        }

    def calculate_dynamic_d( self ): # "((G79*K151)+(G80*K153)+(G81*K157))"
        myArray = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "feedUsageInformation" ];

        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] * item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "((G79*K151)+(G80*K153)+(G81*K157))"
        }

    def calculate_dynamic_e( self ): # "((G90*K174)+(G91*K176)+(G92*K178))"
        myArray = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "drugsUsageInformation" ];

        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] * item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "((G79*K151)+(G80*K153)+(G81*K157))"
        }

    def calculate_dynamic_f( self ): # "((L48*G99)+(L50*G100)+(L52*G101))/L10"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "fuelForTemperatureControlInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] + item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "((L48*G99)+(L50*G100)+(L52*G101))"
        }

    def calculate_dynamic_g( self ): # "(L73*L74*G107)+(L76*L77*G108)+(L79*L80*G109)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "pesticidesUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "averageQuantity" ] + item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "(L73*L74*G107)+(L76*L77*G108)+(L79*L80*G109)"
        }

    def calculate_dynamic_h( self ): # "(L95*L96*G111)+(L102*L103*G112)+(L109*L110*G113)"
        # self.printAlert( 176 );
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            # print( "averageQuantity : " + str( item[ "averageQuantity" ] ) + ", productPrice : " + str( item[ "productPrice" ] ) + " , numberOfTreatments : " + str( item[ "numberOfTreatments" ] ) );
            myTotal += item[ "averageQuantity" ] * 1000 * item[ "productPrice" ] * item[ "numberOfTreatments" ];
        # print( "---------------------------- END ----------------------------" );
        return { 
          "result"     : myTotal , 
          "expression" : "(L95*L96*G111)+(L102*L103*G112)+(L109*L110*G113)"
        }

    def calculate_dynamic_i( self ): # "(G115*L139+G116*L141+G117*L143)"
        # self.printAlert( 189 );
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "feedUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] * item[ "numberOfTreatments" ] * item[ "productPrice" ];
        #     print( 
        #         "quantity : " + str( item[ "quantity" ] ) + 
        #         ", numberOfTreatments : " + str( item[ "numberOfTreatments" ] ) + 
        #         ", productPrice : " + str( item[ "productPrice" ] ) 
        #     );
        # print( "---------------------------- END ----------------------------" );

        return { 
          "result"     : myTotal , 
          "expression" : "(G115*L139+G116*L141+G117*L143)"
        }

    def calculate_dynamic_j( self ): # "(G119*L162+G120*L164+G121*L166)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "drugsUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] + item[ "productPrice" ];

        return { 
          "result"     : myTotal , 
          "expression" : "(G119*L162+G120*L164+G121*L166)"
        }

    def calculate_dynamic_k( self ): # "(K174+K176+K178)/K17"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "drugsUsageInformation" ];
        nOfAnimals         = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "parcelInformation" ][ "numberOfAnimals" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ];
        
        if nOfAnimals is None :
            return { 
              "result"     : 0, 
              "expression" : "(K174+K176+K178)/K17"          }
        else:
            return { 
              "result"     : myTotal / nOfAnimals, 
              "expression" : "(K174+K176+K178)/K17"
            }

    def calculate_dynamic_l( self ): # "(K82*K83)+(K85*K86)+(K88*K89)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "pesticidesUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ];

        return { 
          "result"     : myTotal , 
          "expression" : "(K82*K83)+(K85*K86)+(K88*K89)"
        }

    def calculate_dynamic_m( self ): # "K95*K96*(K99/100)+K102*K103*(K106/100)+K109*K110*(K113/100)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averagePotassiumQuantity" ] / 100 );

        return { 
          "result"     : myTotal , 
          "expression" : "K95*K96*(K99/100)+K102*K103*(K106/100)+K109*K110*(K113/100)"
        }

    def calculate_dynamic_n( self ): # "K95*K96*(K98/100)+K102*K103*(K105/100)+K109*K110*(K112/100)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averagePhosphorusQuantity" ] / 100 );

        return { 
          "result"     : myTotal , 
          "expression" : "K95*K96*(K98/100)+K102*K103*(K105/100)+K109*K110*(K112/100)"
        }

    def calculate_dynamic_o( self ): # "K95*K96*(K97/100)+K102*K103*(K104/100)+K109*K110*(K111/100)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averageNitrogenQuantity" ] / 100 );

        return { 
          "result"     : myTotal , 
          "expression" : "K95*K96*(K97/100)+K102*K103*(K104/100)+K109*K110*(K111/100)"
        }

    def calculate_dynamic_p( self ): # "L95*L96*(L97/100)+L102*L103*(L104/100)+L109*L110*(L111/100)"
        # myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "fertilizersUsageInformation" ];
        # myTotal = 0;
        # for item in myArray:
            # print( "averageQuantity : " + str( item[ "averageQuantity" ] ) + ", productPrice : " + str( item[ "productPrice" ] ) + " , numberOfTreatments : " + str( item[ "numberOfTreatments" ] ) );
            # myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averagePotassiumQuantity" ] / 100 );

        # print( "--------------------- CUSTOM FUNCTIONS ----------------------" );
        # print( "-------------------- customFunctions.py ---------------------" );
        # print( "------------------------ Line:276 ---------------------------" );
        # print( "------------------------- FORMULA ---------------------------" );
        # self.printAlert( 291 );
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            # print( "numberOfTreatments : " + str( item[ "numberOfTreatments" ] ) + ", averageQuantity : " + str( item[ "averageQuantity" ] ) + " , averageNitrogenQuantity : " + str( item[ "averageNitrogenQuantity" ] ) );
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averageNitrogenQuantity" ] / 100 );
        # print( "---------------------------- END ----------------------------" );

        return { 
          "result"     : myTotal , 
          "expression" : "K95*K96*(K99/100)+K102*K103*(K106/100)+K109*K110*(K113/100)"
        }

    def calculate_dynamic_q( self ): # "L95*L96*(L98/100)+L102*L103*(L105/100)+L109*L110*(L112/100)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averagePhosphorusQuantity" ] / 100 );

        return { 
          "result"     : myTotal , 
          "expression" : "K95*K96*(K98/100)+K102*K103*(K105/100)+K109*K110*(K112/100)"
        }

    def calculate_dynamic_r( self ): # "L95*L96*(L99/100)+L102*L103*(L106/100)+L109*L110*(L113/100)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "fertilizersUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ] * ( item[ "averagePotassiumQuantity" ] / 100 );

        return { 
          "result"     : myTotal , 
          "expression" : "K95*K96*(K97/100)+K102*K103*(K104/100)+K109*K110*(K111/100)"
        }

    def calculate_dynamic_s( self ): # "(L73*L74)+(L76*L77)+(L79*L80)"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "pesticidesUsageInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "numberOfTreatments" ] * item[ "averageQuantity" ];

        return { 
          "result"     : myTotal , 
          "expression" : "(L73*L74)+(L76*L77)+(L79*L80)"
        }

    def calculate_dynamic_t( self ): # "(L162+L164+L166)/L17"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "drugsUsageInformation" ];
        nOfAnimals         = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "parcelInformation" ][ "numberOfAnimals" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ];

        return { 
          "result"     : myTotal / nOfAnimals, 
          "expression" : "(L162+L164+L166)/L17"
        }

    def calculate_dynamic_u( self ): # "(L162+L164+L166)/L17"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "drugsUsageInformation" ];
        nOfAnimals         = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "parcelInformation" ][ "numberOfAnimals" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ];

        if nOfAnimals is None :
            return { 
              "result"     : 0, 
              "expression" : "(K174+K176+K178)/K17"          }
        else:
            return { 
              "result"     : myTotal / nOfAnimals, 
              "expression" : "(L162+L164+L166)/L17"
            }

    def calculate_dynamic_v( self ): # "(L162+L164+L166)/L20"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "drugsUsageInformation" ];
        nOfAnimals         = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "parcelInformation" ][ "aquacultureArea" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ];

        if nOfAnimals is None :
            return { 
              "result"     : 0, 
              "expression" : "(K174+K176+K178)/K17"          }
        else:
            return { 
              "result"     : myTotal / nOfAnimals, 
              "expression" : "(L162+L164+L166)/L20"
            }

    def calculate_dynamic_w( self ): # "(L162+L164+L166)/L19"
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "drugsUsageInformation" ];
        nOfAnimals         = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ "parcelAssessmentWithoutDATS" ][ "parcelInformation" ][ "numberOfBeehives" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ];

        if nOfAnimals is None :
            return { 
              "result"     : 0, 
              "expression" : "(K174+K176+K178)/K17"          }
        else:
            return { 
              "result"     : myTotal / nOfAnimals, 
              "expression" : "(L162+L164+L166)/L19"
            }

    def calculate_dynamic_x( self ): # "((D23+D24)+(I23+I24)+(M23+M24))"
        myArray            = self.UserInputs[ "datsInformation" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "datsAnnualFees" ] + item[ "datsInitialInvestmentCosts" ] + item[ "datsTrainingCosts" ];

        return { 
          "result"     : myTotal , 
          "expression" : "((D23+D24)+(I23+I24)+(M23+M24))"
        }

    def getData( self , withDATs = True ):
        ivaylosJSONParentName = "parcelAssessmentWithDATS" if withDATs is True else "parcelAssessmentWithoutDATS";
        myArray            = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ ivaylosJSONParentName ][ "fuelForTemperatureControlInformation" ];
        myparcelDimensions = self.UserInputs[ "yearlyAssessmentInformation" ][ self.yearIndex ][ "parcelComparison" ][ 0 ][ ivaylosJSONParentName ][ "parcelInformation" ][ "parcelDimension" ];
        myTotal = 0;
        for item in myArray:
            myTotal += item[ "quantity" ] + item[ "productPrice" ];

        return { 
          "result"     : myTotal / myparcelDimensions , 
          "expression" : "((L48*G99)+(L50*G100)+(L52*G101))/L10"
        }