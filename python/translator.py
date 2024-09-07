class BrailleTranslator:

    BRAILLE_LETTER = ['.', '0']

    LETTER_BRAILLE_MAP = {
        "A": 1,
        "B": 13,
        "C": 12,
        "D": 124,
        "E": 14,
        "F": 123,
        "G": 1234,
        "H": 134,
        "I": 23,
        "J": 234,
        "K": 15,
        "L": 135,
        "M": 125,
        "N": 1245,
        "O": 145,
        "P": 1235,
        "Q": 12345,
        "R": 1345,
        "S": 235,
        "T": 2345,
        "U": 156,
        "V": 1356,
        "W": 2346,
        "X": 1256,
        "Y": 12456,
        "Z": 1456,
    }

    DIGIT_BRAILLE_MAP = {
        "1": LETTER_BRAILLE_MAP["A"],
        "2": LETTER_BRAILLE_MAP["B"],
        "3": LETTER_BRAILLE_MAP["C"],
        "4": LETTER_BRAILLE_MAP["D"],
        "5": LETTER_BRAILLE_MAP["E"],
        "6": LETTER_BRAILLE_MAP["F"],
        "7": LETTER_BRAILLE_MAP["G"],
        "8": LETTER_BRAILLE_MAP["H"],   
        "9": LETTER_BRAILLE_MAP["I"],
        "0": LETTER_BRAILLE_MAP["J"],
    }

    '''Symbols that change the meaning of a sentence in braille.'''
    BRAILLE_MODIFIERS = {
        "CAPITAL_FOLLOW": 6,
        "DECIMAL_FOLLOW": 26,
        "NUMBER_FOLLOW": 2456,
    }

    BRAILLE_SPECIAL_MAP = {
        ".": 346,
        ",": 3,
        "?": 356,
        "!": 345,
        ":": 34,
        ";": 35,
        "-": 56,
        "/": 25,
        "<": 236,
        ">": 145,
        "(": 136,
        ")": 245,
        " ": 000000,
    }

    INVERSE_LETTER_BRAILLE_MAP = {}
    INVERSE_DIGIT_BRAILLE_MAP = {}
    INVERSE_BRAILLE_MODIFIERS = {}
    INVERSE_BRAILLE_SPECIAL_MAP = {}

    BRAILLE_CHARSET = set()

    def __init__(self) -> None:
        self.LETTER_BRAILLE_MAP = self.__pad_braille_map(self.LETTER_BRAILLE_MAP)
        self.DIGIT_BRAILLE_MAP = self.__pad_braille_map(self.DIGIT_BRAILLE_MAP)
        self.BRAILLE_MODIFIERS = self.__pad_braille_map(self.BRAILLE_MODIFIERS)
        self.BRAILLE_SPECIAL_MAP = self.__pad_braille_map(
            self.BRAILLE_SPECIAL_MAP
        )
        self.BRAILLE_CHARSET = set()\
        .union(set(self.LETTER_BRAILLE_MAP.values())) \
        .union(set(self.DIGIT_BRAILLE_MAP.values())) \
        .union(set(self.BRAILLE_MODIFIERS.values())) \
        .union(set(self.BRAILLE_SPECIAL_MAP.values())) \

        # Define the inverses
        self.INVERSE_LETTER_BRAILLE_MAP = dict(
            map(reversed, self.LETTER_BRAILLE_MAP.items())
        )
        self.INVERSE_DIGIT_BRAILLE_MAP = dict(
            map(reversed, self.DIGIT_BRAILLE_MAP.items())
        )
        self.INVERSE_BRAILLE_MODIFIERS = dict(
            map(reversed, self.BRAILLE_MODIFIERS.items())
        )
        self.INVERSE_BRAILLE_SPECIAL_MAP =dict(
            map(reversed, self.BRAILLE_SPECIAL_MAP.items())
        )

    def translate(self, message: str) -> str:
        """Translate a message to braille or english depending on the message type.

        Note: translator will default to english braille translation on unsupported 
        braille symbols.

        :param message: A message that is in either braille or english.
        :type message: str
        :return: str A translated message opposite of the original word language.
        :rtype: bool
        """

        if(self.__is_braille(message)):
            return self.__braille_to_english(message)
        return self.__english_to_braille(message)
    

    def is_braille(self, message: str) -> bool:
        return self.__is_braille(message)

    def __is_braille(self, message: str) -> bool:
        """Checks if message is written in the braille language

        A message is written braille if it meets the following criteria:
            1. The message length is a multiple of 6
            2. All characters are either `O` or `.`
            3. Every 6 char grouping correspond to a braille symbol. 
         
        :param message: The message to inspect.
        :type message: str
        :return: True if the message is in Braille format, False otherwise.
        :rtype: bool
        """

        message_size = len(message)
        valid_braille_size = message_size % 6 == 0
        if (not valid_braille_size):
            return False
        
        message_chunks = []
        for chunk_pos in range(0, message_size, 6):
            chunk = message[chunk_pos: chunk_pos+6]
            message_chunks.append(chunk)
        
        valid_chunk = all(chunk in self.BRAILLE_CHARSET \
                          for chunk in message_chunks)
        #Condition 3 implies condition 2
        return valid_chunk


    def __braille_to_english(self, message: str) -> str:
        '''Converts braille message to english

        Preconditions:
            1. Message cannot end on a modifier. (capital / number) follows 
            2. A decimal modifier must come after a number modifier to \
                denote a decimal digit

        :param message: The message to translate.
        :type message: str
        :return: A english translation of the message.
        :rtype: str
        '''
        message_size = len(message)
        message_chunks = []
        for chunk_pos in range(0, message_size, 6):
            chunk = message[chunk_pos: chunk_pos+6]
            message_chunks.append(chunk)

    
        translated_message = ""
        chunk_size = len(message_chunks)
        pos = 0

        is_space = lambda w: w == self.BRAILLE_SPECIAL_MAP.get(" ")
        is_letter = lambda w: w in self.INVERSE_LETTER_BRAILLE_MAP 
        is_number = lambda w: w == self.BRAILLE_MODIFIERS.get("NUMBER_FOLLOW")
        is_capital = lambda w: w == self.BRAILLE_MODIFIERS.get("CAPITAL_FOLLOW")
        is_decimal = lambda w: w == self.BRAILLE_MODIFIERS.get("DECIMAL_FOLLOW")
        is_special = lambda w: w in self.INVERSE_BRAILLE_SPECIAL_MAP 
        in_number_group = lambda w: w in self.INVERSE_DIGIT_BRAILLE_MAP
        in_decimal_group = lambda w: in_number_group(w) or is_decimal(w) \
            and not is_space(w)

        current_context = None

        while(pos < chunk_size):
            braille_symbol = message_chunks[pos]
            
            if(is_space(braille_symbol)):
                current_context = None
                translated_message += " "
                pos += 1
                continue

            elif(is_letter(braille_symbol)):
                translated_message += self.INVERSE_LETTER_BRAILLE_MAP.get(
                    braille_symbol
                ).lower()
                pos += 1
                continue

            elif(is_capital(braille_symbol)):
                valid_bound = pos + 1 < chunk_size
                if(not valid_bound):
                    raise Exception("Cannot capitalize a non-existing letter")
                capital_symbol = message_chunks[pos + 1]
                valid_letter = is_letter(capital_symbol)
                if(not valid_letter):
                    raise Exception(f'Unknown braille symbol detected \
                        during capitalization = {capital_symbol} \n at position {pos+1}')
                translated_message += self.INVERSE_LETTER_BRAILLE_MAP.get(
                    capital_symbol
                )
                # Since we processed 2 braille symbols. (Modifier and letter)
                pos += 2
                continue

            elif(is_number(braille_symbol)):
                valid_bound = pos + 1 < chunk_size
                if(not valid_bound):
                    raise Exception("Non-existing digit at EOL at position ...")
                current_digit = message_chunks[pos + 1]
                valid_number = in_number_group(current_digit)
                if(not valid_number):
                    if(is_decimal(current_digit)):
                        raise Exception("Number modifier cannot directly preceed \
                             decimal modifier.")
                    raise Exception(f'Unknown braille number symbol at position ${pos+1}')
                right = pos + 1
                chunk = ""
                while(right < chunk_size and in_decimal_group(message_chunks[right])):
                    current_digit = self.INVERSE_DIGIT_BRAILLE_MAP.get(message_chunks[right])
                    if(current_digit is None):
                        if(is_decimal(message_chunks[right])):
                            chunk += "."
                        else:
                            print(self.BRAILLE_MODIFIERS.get("DECIMAL_FOLLOW"))
                            print(current_digit)
                            print(is_decimal(current_digit))
                            raise Exception(f'Unknown Digit Symbol ${message_chunks[right]} \
                                            at position ${right}')
                    else:
                        chunk += current_digit
                
                    right += 1 

                translated_message += chunk
                pos = right
                continue
            elif(is_special(braille_symbol)):
                translated_message += self.INVERSE_BRAILLE_SPECIAL_MAP.get(
                    braille_symbol
                )
                pos += 1
                continue
            raise Exception(f'Unhandled state while processing symbol {braille_symbol} \nat \
                position ${pos} in during translation')

        return translated_message
    

    def __english_to_braille(self, message: str) -> str:
        """Converts message to braille.

        A message is coverted to braille with the following assumption:
            1. Each message symbol is mapped to an equivalent braille symbol
            2. A sequence of symbols may have a context modifier appended
                1. `CAPITAL_FOLLOW` only if the next symbol is capitalized
                2. `NUMBER_FOLLOW` if the next symbol is a number.
            3. Letter and number cannot be in the same context group, ex: `1a`
            4. Decimals cannot start without a preceeding digit otherwise
            it will be interpetered as a period. ex: `.7`

        :param message: The message to translate.
        :type message: str
        :return: A Braille translation of message.
        :rtype: str
        """

        is_letter = lambda w: w in self.LETTER_BRAILLE_MAP
        is_digit = lambda w: w in self.DIGIT_BRAILLE_MAP  
        is_special = lambda w: w in self.BRAILLE_SPECIAL_MAP
        is_decimal = lambda w: w == "."
        in_number_group = lambda symbol : symbol.isdigit() or is_decimal(symbol) \
             and symbol != " "
        

        braille_message = ""
        message_size = len(message)
        pos = 0

        while(pos < message_size):
            english_symbol = message[pos]
            if(is_letter(english_symbol.upper())):
                braille_symbol = self.LETTER_BRAILLE_MAP.get(english_symbol.upper())
                if(english_symbol.isupper()):
                    braille_message += self.BRAILLE_MODIFIERS["CAPITAL_FOLLOW"] + \
                         braille_symbol
                else:
                    braille_message += braille_symbol
                pos += 1
                continue

            elif(is_digit(english_symbol)):
                #Expand until there are no more digits.
                chunk = ""
                right = pos
                while(right < message_size and in_number_group(message[right])):
                    braille_symbol = self.DIGIT_BRAILLE_MAP.get(message[right])
                    if(braille_symbol is None):
                        if(is_decimal(message[right])):
                            chunk += self.BRAILLE_MODIFIERS["DECIMAL_FOLLOW"]
                        else:
                            raise Exception(f'Unknown Digit Symbol {message[right]} \
                                        at position ${right}')
                    else:
                        chunk += braille_symbol
                    right += 1

                braille_message += self.BRAILLE_MODIFIERS["NUMBER_FOLLOW"] + chunk
                pos = right
                continue
            
            elif(is_special(english_symbol)):
                braille_symbol = self.BRAILLE_SPECIAL_MAP.get(english_symbol)
                braille_message += braille_symbol
                pos += 1
                continue
            else:
                raise Exception(f'Unhandled state while processing symbol {message[pos]} \nat \
                                position ${pos} in during translation')

        return braille_message



    def __pad_braille_map(self, pad_mapping: dict[str,int]) -> dict[str, str]:
        """Converts braille pad number mapping to a braille string mapping

        Braille pad numbers corrospond to the markings on a 2x6 grid.
        The ordering of digit has no effect on the output. 
            - Example: 251 and 152 both map to the same padding.
        
        If a digit is present in the braille pad number then it corrosponds to
        raised dot at a position.

        :param pad_mapping: A string to pad number mapping.
        :type pad_mapping: dict[str,int]
        :return: A string to braille mapping. 
        :rtype: dict[str, str]
        """

        brail_map = {}
        for k,v in pad_mapping.items():
            brail_map[k] = self.__pad_number_to_braille_map(v)
        return brail_map
    
    def __pad_number_to_braille_map(self, pad_number: int) -> str:
        '''
        Converts a pad number to braille.
        A pad number contains the cell positions to mark on a 2x6 
        grid.

        :param pad_number: a pad number thats to be converted.
        :type pad_number: str
        :return: A string to braille mapping. 
        :rtype: int
        '''

        transform = ["."] * 6
        rtext = [int(c) for c in [*str(pad_number)]]
        for position in rtext:
            position_index = position -1 
            if(position_index < 0): 
                continue
            transform[position_index] = "O"
        return ''.join(transform)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
                    prog='translator.py',
                    description='Translate between english and braille',
                    epilog='For the shopify eng-intern-challenge 2025 by Seron Athavan.')
                    
    parser.add_argument('message', metavar='N', type=str, nargs='+',
                    help='A message to translate')
    args = parser.parse_args()
