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
    INVERSE__BRAILLE_SPECIAL_MAP = {}

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
            map(reversed, self.INVERSE_LETTER_BRAILLE_MAP.items())
        )
        self.INVERSE_DIGIT_BRAILLE_MAP = dict(
            map(reversed, self.INVERSE_DIGIT_BRAILLE_MAP.items())
        )
        self.INVERSE_BRAILLE_MODIFIERS = dict(
            map(reversed, self.INVERSE_BRAILLE_MODIFIERS.items())
        )
        self.INVERSE__BRAILLE_SPECIAL_MAP =dict(
            map(reversed, self.INVERSE__BRAILLE_SPECIAL_MAP.items())
        )

    def translate(self, message: str) -> str:
        pass
    

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


    def braille_to_english(self, message: str) -> str:
        return self.__braille_to_english(message)
    

    def __braille_to_english(self, message: str) -> str:
        '''Converts braille message to english

        :param message: The message to translate.
        :type message: str
        :return: A english translation of the message.
        :rtype: bool
        :raise: 
            - `Exception`: if an unknown braille letter is present.
        '''
        message_size = len(message)
        message_chunks = []
        for chunk_pos in range(0, message_size, 6):
            chunk = message[chunk_pos: chunk_pos+6]
            message_chunks.append(chunk)

        
        


        translated_message = ""
        chunk_size = len(message_chunks)
        pos = 0

        while(pos < chunk_size):
            braille_symbol = message_chunks[pos]
            is_space = lambda w: w == self.BRAILLE_SPECIAL_MAP.get(" ")
            is_letter = lambda w: w in self.INVERSE_LETTER_BRAILLE_MAP 
            pass

        return chunk_size
    
    def english_to_braille(self, message: str) -> str:
        return self.__english_to_braille(message)

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
        :raise: 
            - `Exception`: if unsupported symbol is present during translaton.
        """

        in_number_group = lambda symbol : symbol.isdigit() and symbol != " "
        
        braille_message = ""
        message_size = len(message)
        pos = 0

        while(pos < message_size):
            if(message[pos].isupper()):
                current_modifier = self.BRAILLE_MODIFIERS["CAPITAL_FOLLOW"]
                braille_symbol = self.LETTER_BRAILLE_MAP.get(message[pos])
                if(braille_symbol is None):
                    raise Exception(f'Unknown Capital Symbol ${message[pos]} \
                                    at position ${pos}')
                braille_message += current_modifier + braille_symbol
                pos += 1
                continue

            elif(message[pos].isdigit()):
                #Expand until there are no more digits.
                current_modifier = self.BRAILLE_MODIFIERS["NUMBER_FOLLOW"]
                chunk = ""
                right = pos
                while(right < message_size and in_number_group(message[right])):
                    braille_symbol = self.DIGIT_BRAILLE_MAP.get(message[right])
                    if(braille_symbol is None):
                        raise Exception(f'Unknown Digit Symbol ${message[right]} \
                                        at position ${right}')
                    chunk += braille_symbol
                    right += 1

                braille_message += current_modifier + chunk
                pos = right
                continue

            elif(message[pos].isspace()):
                current_modifier = None
                braille_symbol = self.BRAILLE_SPECIAL_MAP.get(message[pos])
                braille_message += braille_symbol
                pos += 1
                continue

            elif(message[pos].isalpha()):
                current_modifier = None
                mkey = message[pos].upper()
                braille_symbol = self.LETTER_BRAILLE_MAP.get(mkey)
                braille_message += braille_symbol
                pos += 1
                continue
            else:
                raise Exception(f'Unknown symbol ${message[pos]} at \
                                position ${pos} in during translation')

        return braille_message



    def __pad_braille_map(self, pad_mapping: dict[str,int]) -> dict[str, str]:
        '''
        Converts the pad number values to its equilvant braille number.
        '''
        brail_map = {}
        for k,v in pad_mapping.items():
            brail_map[k] = self.__pad_number_to_braille_map(v)
        return brail_map
    
    def __pad_number_to_braille_map(self, pad_number: int) -> str:
        '''
        Converts a pad number to braille.
        A pad number contains the cell positions to mark on a 2x6 
        grid.
        '''
        transform = ["."] * 6
        rtext = [int(c) for c in [*str(pad_number)]]
        for position in rtext:
            position_index = position -1 
            if(position_index < 0): 
                continue
            transform[position_index] = "O"
        return ''.join(transform)

translator = BrailleTranslator()