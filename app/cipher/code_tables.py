def code_table_e(text, table_dict, bin_swap_dict, bin_code=False, delimiter=" "):
    from .common import replace_all
    converted = ""

    for s in text[:]:
        if s in table_dict:
            converted += table_dict[s] + delimiter
        else:
            converted += s + delimiter

    if bin_code:
        converted = replace_all(converted, bin_swap_dict)

    return converted


def code_table_d(text, table_dict, bin_swap_dict, bin_code=False, delimiter=" "):
    from .common import replace_all
    if bin_code:
        table_dict_inv = dict((replace_all(j, bin_swap_dict), i)
                              for (i, j) in table_dict.items())
    else:
        table_dict_inv = dict((j, i) for (i, j) in table_dict.items())

    text_rows = text.split('\n')

    decoded_rows = []
    for text_row in text_rows:
        code_string = text_row.split(delimiter)
        decoded_row = ""
        for s in code_string:
            if s in table_dict_inv:
                decoded_row += table_dict_inv[s]
            elif len(s) > 0:
                decoded_row += "[" + s + "]"
        decoded_rows.append(decoded_row)

    return '\n'.join(decoded_rows)


list_A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
list_a = list_A.lower()
list_0 = "0123456789"
list_0_for_atbash = "123456789"
list_hex = "0123456789abcdef"
list_base36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
polybius_table = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

morse_code_table = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',  'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    '0': '-----',  '1': '.----',  '2': '..---', '3': '...--',  '4': '....-',
    '5': '.....', '6': '-....',  '7': '--...',  '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', ':': '---...', '?': '..--..',
    "'": '.----.', '-': '-....-', '/': '-..-.', '@': '.--.-.', '=': '-...-',
    ' ': '/'
}

morse_wabun_code_table = {
    'イ': '.-', 'ロ': '.-.-', 'ハ': '-...', 'ニ': '-.-.', 'ホ': '-..',
    'ヘ': '.', 'ト': '..-..', 'チ': '..-.', 'リ': '--.', 'ヌ': '....',
    'ル': '-.--.', 'ヲ': '.---', 'ワ': '-.-', 'カ': '.-..', 'ヨ': '--',
    'タ': '-.', 'レ': '---', 'ソ': '---.', 'ツ': '.--.', 'ネ': '--.-',
    'ナ': '.-.', 'ラ': '...', 'ム': '-', 'ウ': '..-', 'ヰ': '.-..-',
    'ノ': '..--', 'オ': '.-...', 'ク': '...-', 'ヤ': '.--', 'マ': '-..-',
    'ケ': '-.--', 'フ': '--..', 'コ': '----', 'エ': '-.---', 'テ': '.-.--',
    'ア': '--.--', 'サ': '-.-.-', 'キ': '-.-..', 'ユ': '-..--', 'メ': '-...-',
    'ミ': '..-.-', 'シ': '--.-.', 'ヱ': '.--..', 'ヒ': '--..-', 'モ': '-..-.',
    'セ': '.---.', 'ス': '---.-', 'ン': '.-.-.', '゛': '..', '゜': '..--.',
    'ー': '.--.-', '、': '.-.-.-', '」': '.-.-..', '（': '-.--.-', '）': '.-..-.',
    '0': '-----',  '1': '.----',  '2': '..---', '3': '...--',  '4': '....-',
    '5': '.....', '6': '-....',  '7': '--...',  '8': '---..', '9': '----.',
}

bacon1_table = {
    'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
    'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaaa',
    'K': 'abaab', 'L': 'ababa', 'M': 'ababb', 'N': 'abbaa', 'O': 'abbab',
    'P': 'abbba', 'Q': 'abbbb', 'R': 'baaaa', 'S': 'baaab', 'T': 'baaba',
    'U': 'baabb', 'V': 'baabb', 'W': 'babaa', 'X': 'babab', 'Y': 'babba', 'Z': 'babbb',
    ' ': '/'
}

bacon2_table = {
    'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
    'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
    'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
    'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
    'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab',
    ' ': '/'
}

abc012_table = {
    'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4',
    'F': '5', 'G': '6', 'H': '7', 'I': '8', 'J': '9',
    'K': '10', 'L': '11', 'M': '12', 'N': '13', 'O': '14',
    'P': '15', 'Q': '16', 'R': '17', 'S': '18', 'T': '19',
    'U': '20', 'V': '21', 'W': '22', 'X': '23', 'Y': '24', 'Z': '25',
    ' ': '/'
}

# International Radiotelephony Spelling Alphabet (NATO phonetic alphabet)
spelling_alphabet_icao_2008 = {
    'a': 'alfa', 'b': 'bravo', 'c': 'charlie', 'd': 'delta', 'e': 'echo', 'f': 'foxtrot', 'g': 'golf', 'h': 'hotel', 'i': 'india', 'j': 'juliett', 'k': 'kilo', 'l': 'lima', 'm': 'mike', 'n': 'november', 'o': 'oscar', 'p': 'papa', 'q': 'quebec', 'r': 'romeo', 's': 'sierra', 't': 'tango', 'u': 'uniform', 'v': 'victor', 'w': 'whiskey', 'x': 'x-ray', 'y': 'yankee', 'z': 'zulu'
}

# 1951 ICAO code words
spelling_alphabet_icao_1951 = {
    'a': 'alfa', 'b': 'bravo', 'c': 'coca', 'd': 'delta', 'e': 'echo', 'f': 'foxtrot', 'g': 'gold', 'h': 'hotel', 'i': 'india', 'j': 'juliett', 'k': 'kilo', 'l': 'lima', 'm': 'metro', 'n': 'nectar', 'o': 'oscar', 'p': 'papa', 'q': 'quebec', 'r': 'romeo', 's': 'sierra', 't': 'tango', 'u': 'union', 'v': 'victor', 'w': 'whiskey', 'x': 'extra', 'y': 'yankee', 'z': 'zulu'
}

# 1949 ICAO code words
spelling_alphabet_icao_1949 = {
    'a': 'alfa', 'b': 'beta', 'c': 'coca', 'd': 'delta', 'e': 'echo', 'f': 'foxtrot', 'g': 'golf', 'h': 'hotel', 'i': 'india', 'j': 'julietta', 'k': 'kilo', 'l': 'lima', 'm': 'metro', 'n': 'nectar', 'o': 'oscar', 'p': 'papa', 'q': 'quebec', 'r': 'romeo', 's': 'sierra', 't': 'tango', 'u': 'union', 'v': 'victor', 'w': 'whiskey', 'x': 'x-ray', 'y': 'yankee', 'z': 'zebra'
}

# 1947 ICAO Latin America/Caribbean
spelling_alphabet_icao_1947_1 = {
    'a': 'ana', 'b': 'brazil', 'c': 'coco', 'd': 'dado', 'e': 'elsa', 'f': 'fiesta', 'g': 'gato', 'h': 'hombre', 'i': 'india', 'j': 'julio', 'k': 'kilo', 'l': 'luis', 'm': 'mama', 'n': 'norma', 'o': 'opera', 'p': 'peru', 'q': 'quebec', 'r': 'rosa', 's': 'sara', 't': 'tomas', 'u': 'uruguay', 'v': 'victor', 'w': 'whiskey', 'x': 'equis', 'y': 'yolanda', 'z': 'zeta'
}

# 1947 ICAO alphabet (adopted exactly from ARRL)
spelling_alphabet_icao_1947_2 = {
    'a': 'adam', 'b': 'baker', 'c': 'charlie', 'd': 'david', 'e': 'edward', 'f': 'freddie', 'g': 'george', 'h': 'harry', 'i': 'ida', 'j': 'john', 'k': 'king', 'l': 'luis', 'm': 'mama', 'n': 'norma', 'o': 'opera', 'p': 'peru', 'q': 'quebec', 'r': 'rosa', 's': 'sara', 't': 'tomas', 'u': 'uruguay', 'v': 'victor', 'w': 'whiskey', 'x': 'equis', 'y': 'yolanda', 'z': 'zeta'
}

# Chemical Symbol
chemical_symbol = {
    '1': 'H', '2': 'He', '3': 'Li', '4': 'Be', '5': 'B', '6': 'C', '7': 'N', '8': 'O', '9': 'F', '10': 'Ne', '11': 'Na', '12': 'Mg', '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl', '18': 'Ar', '19': 'K', '20': 'Ca', '21': 'Sc', '22': 'Ti', '23': 'V', '24': 'Cr', '25': 'Mn', '26': 'Fe', '27': 'Co', '28': 'Ni', '29': 'Cu', '30': 'Zn', '31': 'Ga', '32': 'Ge', '33': 'As', '34': 'Se', '35': 'Br', '36': 'Kr', '37': 'Rb', '38': 'Sr', '39': 'Y', '40': 'Zr', '41': 'Nb', '42': 'Mo', '43': 'Tc', '44': 'Ru', '45': 'Rh', '46': 'Pd', '47': 'Ag', '48': 'Cd', '49': 'In', '50': 'Sn', '51': 'Sb', '52': 'Te', '53': 'I', '54': 'Xe', '55': 'Cs', '56': 'Ba', '57': 'La', '58': 'Ce', '59': 'Pr', '60': 'Nd', '61': 'Pm', '62': 'Sm', '63': 'Eu', '64': 'Gd', '65': 'Tb', '66': 'Dy', '67': 'Ho', '68': 'Er', '69': 'Tm', '70': 'Yb', '71': 'Lu', '72': 'Hf', '73': 'Ta', '74': 'W', '75': 'Re', '76': 'Os', '77': 'Ir', '78': 'Pt', '79': 'Au', '80': 'Hg', '81': 'Tl', '82': 'Pb', '83': 'Bi', '84': 'Po', '85': 'At', '86': 'Rn', '87': 'Fr', '88': 'Ra', '89': 'Ac', '90': 'Th', '91': 'Pa', '92': 'U', '93': 'Np', '94': 'Pu', '95': 'Am', '96': 'Cm', '97': 'Bk', '98': 'Cf', '99': 'Es', '100': 'Fm', '101': 'Md', '102': 'No', '103': 'Lr', '104': 'Rf', '105': 'Db', '106': 'Sg', '107': 'Bh', '108': 'Hs', '109': 'Mt', '110': 'Ds', '111': 'Rg', '112': 'Cn', '113': 'Nh', '114': 'Fl', '115': 'Mc', '116': 'Lv', '117': 'Ts', '118': 'Og'
}

braille_table = {
    '000000': '20',    '011101': '21',    '000010': '22',    '001111': '23',    '110101': '24',
    '100101': '25',    '111101': '26',    '001000': '27',    '111011': '28',    '011111': '29',
    '100001': '2A',    '001101': '2B',    '000001': '2C',    '001001': '2D',    '000101': '2E',
    '001100': '2F',    '001011': '30',    '010000': '31',    '011000': '32',    '010010': '33',
    '010011': '34',    '010001': '35',    '011010': '36',    '011011': '37',    '011001': '38',
    '001010': '39',    '100011': '3A',    '000011': '3B',    '110001': '3C',    '111111': '3D',
    '001110': '3E',    '100111': '3F',    '000100': '40',    '100000': '41',    '110000': '42',
    '100100': '43',    '100110': '44',    '100010': '45',    '110100': '46',    '110110': '47',
    '110010': '48',    '010100': '49',    '010110': '4A',    '101000': '4B',    '111000': '4C',
    '101100': '4D',    '101110': '4E',    '101010': '4F',    '111100': '50',    '111110': '51',
    '111010': '52',    '011100': '53',    '011110': '54',    '101001': '55',    '111001': '56',
    '010111': '57',    '101101': '58',    '101111': '59',    '101011': '5A',    '010101': '5B',
    '110011': '5C',    '110111': '5D',    '000110': '5E',    '000111': '5F',
}
