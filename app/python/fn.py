import base64
import binascii
import hashlib

from .transposition import *
from .common import *
from .code_tables import *
from .base_conversion import *
from .math import *
from .enigma import enigma, plugboard_gen
from .purple import purple_decode, purple_encode
from .misc import *


def decode_help():
    txt = '''Decode method HELP:
        rot_a(c,k) : 1文字のみのRot. c:text, k:Rot num, , nc:number convert flag
        vig_a(c,k,type) : 1文字のみのVig. c:text, k:key, type:"d"ならdecode, その他encode
        rot(c,k) : Rot. c:text, k:Rot num
        vig_e(c,k,nc=False), vig_d(c,k,nc=False), beaufort(c,k,nc=False): Vig encode & decode, Beaufort. c:text, k:key, nc:number convert flag
        vig_e_auto(c,k,nc=False), vig_d_auto(c,k,nc=False): Auto key Vig encode & decode. c:text, k:key, nc:number convert flag
        rev(c) : Reverse
        kw(lregexp) : 正規表現にマッチする
        atbash(c, nc:number convert flag)
        playfair_a(c,mode,mx) :2文字のみのPlayfair. c:text, mode:"d"ならdecode, その他encode, mx:Matrixのサイズ。デフォルトは5だが6*6も同様に計算できる。
        playfair_e, playfair_d(text)
        playfair_d6: 6*6matrixのplayfair
        adfgx_e, adfgx_d(text, table_keyword, transposition_keyword)
        adfgvx_e, adfgvx_d(text, table_keyword, transposition_keyword)
        morse_d, morse_e (text, bin_code=False, delimiter=" ") : bin_code == Trueの場合、-.の代わりに01を使用したMorse. 
        bacon1_d, bacon1_e, bacon2_d, bacon2_e : Bacon cipher. 入力の仕方はmorseと同じ。Bacon1はIとJ, UとVを同一視する。Bacon2はいずれも別々に処理。 
        columnar_e, columnar_d (c,col) : colには順番のリストを入れる。キーワードからassign_digits(x)で生成できる
        affine_e(text, a, b), affine_d(text, a, b): aは掛け算、bは足し算部分
        railfence_e, railfence_d(text, rails, offset=0)
        bifid_e, bifid_d(text, table_keyword="")
        abc012(text)
        hexbash(c)
        enigma(text, rotor_left_id, rotor_mid_id, rotor_right_id, reflector_id, rotor_key,ringsetting_key,plugboard):
            text: encode/decode phrase, roter_*_id: 1-5, reflector_id: A-C, rotor_key: 3 letters (ex. XWB),
                  ringsetting_key: 3 letters (ex. FVN), plugboard: letter paris list (ex. ['PO', 'ML', 'IU'])  
        purple_encode, purple_decode (text, sixes_switch_position, twenties_switch_1_position, twenties_switch_2_position, twenties_switch_3_position, plugboard_full, rotor_motion_key): switch_positionは1-6 or 1-25 int, plugboard_fullは26 文字のプラグボード配列, rotor_motion_keyは231等のキーで指示
        text_split(text, step, sep = ' ')
        table_subtitution(text, method) the method should be the right name. See the code for avaliable names.
        '''
    return(txt)


def adfgx_e(text, table_keyword, transposition_keyword):
    table = mixed_alphabet(table_keyword, True)
    letter_set = "ADFGX"
    trimmed_text = text.replace(" ", "").upper().replace("J", "I")

    fractionated = ""
    for s in trimmed_text:
        index = table.index(s)
        row_num = int(index/5)
        col_num = index % 5
        fractionated += letter_set[row_num]
        fractionated += letter_set[col_num]

    return "".join(columnar_e(fractionated, assign_digits(transposition_keyword)))


def adfgx_d(text, table_keyword, transposition_keyword):
    fractionated = columnar_d(text, assign_digits(transposition_keyword))

    table = mixed_alphabet(table_keyword, True)
    letter_set = "ADFGX"

    plain_text = ""
    for i, s in enumerate(fractionated):
        if i % 2 == 0:
            row_num = letter_set.index(s)
        else:
            col_num = letter_set.index(s)
            plain_text += table[row_num*5 + col_num]

    return "".join(plain_text)


def adfgvx_e(text, table_keyword, transposition_keyword):
    table = mixed_alphanumeric(table_keyword)
    letter_set = "ADFGVX"
    trimmed_text = text.replace(" ", "").upper()

    fractionated = ""
    for s in trimmed_text:
        index = table.index(s)
        row_num = int(index/6)
        col_num = index % 6
        fractionated += letter_set[row_num]
        fractionated += letter_set[col_num]

    return "".join(columnar_e(fractionated, assign_digits(transposition_keyword)))


def adfgvx_d(text, table_keyword, transposition_keyword):
    fractionated = columnar_d(text, assign_digits(transposition_keyword))

    table = mixed_alphanumeric(table_keyword)
    letter_set = "ADFGVX"

    plain_text = ""
    for i, s in enumerate(fractionated):
        if i % 2 == 0:
            row_num = letter_set.index(s)
        else:
            col_num = letter_set.index(s)
            plain_text += table[row_num*6 + col_num]

    return "".join(plain_text)


def rot_a(c, k, type="encode"):
    if list_A.find(c) >= 0:
        list = list_A
    elif list_a.find(c) >= 0:
        list = list_a
    elif list_0.find(c) >= 0:
        list = list_0
    else:
        return c

    l = len(list)
    position = list.find(c)

    if type == "encode":
        p = (position + k) % l
    elif type == "decode":
        p = (position - k) % l
    elif type == "beaufort":
        p = (k - position) % l
    else:
        p = c
    return list[p]


def vig_a(c, k, type):
    t = list_A.find(k)
    if t < 0:
        t = list_a.find(k)
    if t < 0:
        t = list_0.find(k)
    if t < 0:
        t = 0
    return rot_a(c, t, type)


def rot(c, k, nc=False):
    l = len(c)
    p = ""
    if nc:
        target = list_A + list_a + list_0
    else:
        target = list_A + list_a

    for i in range(l):
        if c[i] in target:
            p += rot_a(c[i], k)
        else:
            p += c[i]
    return p


def vig_e(c, k, nc=False):
    l_c = len(c)
    l_k = len(k)
    p = ""
    if nc:
        target = list_A + list_a + list_0
    else:
        target = list_A + list_a

    j = 0
    for i in range(l_c):
        if c[i] in target:
            p += vig_a(c[i], k[j], "encode")
            j = (j + 1) % l_k
        else:
            p += c[i]
    return p


def vig_d(c, k, nc=False):
    l_c = len(c)
    l_k = len(k)
    p = ""
    if nc:
        target = list_A + list_a + list_0
    else:
        target = list_A + list_a

    j = 0
    for i in range(l_c):
        if c[i] in target:
            p += vig_a(c[i], k[j], "decode")
            j = (j + 1) % l_k
        else:
            p += c[i]
    return p


def beaufort(c, k, nc=False):
    l_c = len(c)
    l_k = len(k)
    p = ""
    if nc:
        target = list_A + list_a + list_0
    else:
        target = list_A + list_a

    j = 0
    for i in range(l_c):
        if c[i] in target:
            p += vig_a(c[i], k[j], "beaufort")
            j = (j + 1) % l_k
        else:
            p += c[i]
    return p


def vig_e_auto(c, k, nc=False):
    l_c = len(c)
    p = ""
    if nc:
        target = list_A + list_a + list_0
    else:
        target = list_A + list_a
    j = 0
    for i in range(l_c):
        if c[i] in target:
            p += vig_a(c[i], k[j], "encode")
            k += c[i]
            j = j + 1
        else:
            p += c[i]
    return p


def vig_d_auto(c, k, nc=False):
    l_c = len(c)
    p = ""
    if nc:
        target = list_A + list_a + list_0
    else:
        target = list_A + list_a
    j = 0
    for i in range(l_c):
        if c[i] in target:
            p += vig_a(c[i], k[j], "decode")
            k += vig_a(c[i], k[j], "decode")
            j = j + 1
        else:
            p += c[i]
    return p


def kw(regexp):
    import csv
    import re
    kw = open("kw.txt")
    list_all = []
    for row in csv.reader(kw):
        list_all.append(row[0])
    list = [w for w in list_all if re.match(regexp, w)]
    return(list)


def atbash(c, nc=False):
    list_A_atbash = rev(list_A)
    list_a_atbash = list_A_atbash.lower()
    list_0_atbash = rev(list_0_for_atbash)
    tr_A = str.maketrans(list_A, list_A_atbash)
    tr_a = str.maketrans(list_a, list_a_atbash)
    tr_0 = str.maketrans(list_0_for_atbash, list_0_atbash)
    if nc:
        return(c.translate(tr_A).translate(tr_a).translate(tr_0))
    else:
        return(c.translate(tr_A).translate(tr_a))


def hexbash(c):
    c = c.lower()
    list_hex_atbash = rev(list_hex)
    tr_hex = str.maketrans(list_hex, list_hex_atbash)
    return(c.translate(tr_hex))


def playfair_a(c, mode, mx):
    if mode == "d":
        sft = -1
    else:
        sft = 1

    if mx == 6:
        key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    else:
        key = polybius_table
    c = c.upper()
    t0 = key.index(c[0])
    t1 = key.index(c[1])
    t0_r = int(t0/mx)
    t0_c = t0 % mx
    t1_r = int(t1/mx)
    t1_c = t1 % mx
    if t0_r == t1_r and t0_c == t1_c:
        # 同じ文字が連続したときの挙動はrumkinに合わせる。Nianticもそうしていたので・・
        s0 = ((t0_r+sft) % mx)*mx+((t0_c+sft) % mx)
        s1 = ((t1_r+sft) % mx)*mx+((t1_c+sft) % mx)
    elif t0_r == t1_r:
        s0 = t0_r*mx+((t0_c+sft) % mx)
        s1 = t1_r*mx+((t1_c+sft) % mx)
    elif t0_c == t1_c:
        s0 = ((t0_r+sft) % mx)*mx + t0_c
        s1 = ((t1_r+sft) % mx)*mx + t1_c
    else:
        s0 = t0_r*mx+t1_c
        s1 = t1_r*mx+t0_c

    p = key[s0]+key[s1]
    return p


def playfair_e(c):
    c = c.upper().replace("J", "I")
    if len(c) % 2 == 1:
        c += "X"
    p = ""
    for i in range(0, len(c), 2):
        p += playfair_a(c[i:i+2], "e", 5)

    return p


def playfair_d(c):
    c = c.upper().replace("J", "I")
    if len(c) % 2 == 1:
        c += "X"
    p = ""
    for i in range(0, len(c), 2):
        p += playfair_a(c[i:i+2], "d", 5)

    return p


def playfair_e6(c):
    c = c.upper()
    if len(c) % 2 == 1:
        c += "X"
    p = ""
    for i in range(0, len(c), 2):
        p += playfair_a(c[i:i+2], "e", 6)

    return p


def playfair_d6(c):
    c = c.upper()
    if len(c) % 2 == 1:
        c += "X"
    p = ""
    for i in range(0, len(c), 2):
        p += playfair_a(c[i:i+2], "d", 6)

    return p


def polybius_e(text, table_keyword=""):
    table = mixed_alphabet(table_keyword, True)
    text = text.upper().replace("J", "I")
    coordinates = []
    for i in range(len(text)):
        index = table.index(text[i])
        coordinates.append(str(int(index/5)+1))
        coordinates.append(str((index % 5)+1))
    return "".join(coordinates)


def polybius_d(text, table_keyword=""):
    table = mixed_alphabet(table_keyword, True)
    remain = ""
    if len(text) % 2 == 1:
        remain = "[" + text[-1] + "]"
        text = text[0:-1]
    result = [table[(int(text[i])-1)*5 + (int(text[i+1])-1)]
              for i in range(0, len(text), 2)]
    return "".join(result) + remain


def bifid_e(text, table_keyword=""):
    table = mixed_alphabet(table_keyword, True)
    text = text.upper().replace("J", "I")
    coordinates = [[0, 0] for i in range(len(text))]
    for i in range(len(text)):
        index = table.index(text[i])
        coordinates[i] = [int(index/5), index % 5]

    transposed_coordinates = [0]*len(text)*2
    for i in range(len(text)):
        transposed_coordinates[i] = coordinates[i][0]
        transposed_coordinates[i+len(text)] = coordinates[i][1]

    result = ""
    for i in range(len(text)):
        result += table[transposed_coordinates[2*i]
                        * 5+transposed_coordinates[2*i+1]]

    return result


def bifid_d(text, table_keyword=""):
    table = mixed_alphabet(table_keyword, True)
    text = text.upper().replace("J", "I")

    transposed_coordinates = [0]*len(text)*2
    for i in range(len(text)):
        index = table.index(text[i])
        transposed_coordinates[2*i] = int(index/5)
        transposed_coordinates[2*i + 1] = index % 5

    coordinates = [[0, 0] for i in range(len(text))]
    for i in range(len(text)):
        coordinates[i] = [transposed_coordinates[i],
                          transposed_coordinates[i + len(text)]]

    result = ""
    for i in range(len(text)):
        result += table[coordinates[i][0]*5+coordinates[i][1]]

    return result


def morse_e(text, bin_code=False, delimiter=" "):
    text = text.upper()
    return code_table_e(text, morse_code_table, {"-": "0", ".": "1"}, bin_code, delimiter)


def morse_d(text, bin_code=False, delimiter=" "):
    return code_table_d(text, morse_code_table, {"-": "0", ".": "1"}, bin_code, delimiter)


def morse_wabun_e(text, bin_code=False, delimiter=" "):
    text = text.upper()
    return code_table_e(text, morse_wabun_code_table, {"-": "0", ".": "1"}, bin_code, delimiter)


def morse_wabun_d(text, bin_code=False, delimiter=" "):
    return code_table_d(text, morse_wabun_code_table, {"-": "0", ".": "1"}, bin_code, delimiter)


def bacon1_e(text, bin_code=False, delimiter=" "):
    text = text.upper()
    return code_table_e(text, bacon1_table, {"a": "0", "b": "1"}, bin_code, delimiter)


def bacon1_d(text, bin_code=False, delimiter=" "):
    return code_table_d(text, bacon1_table, {"a": "0", "b": "1"}, bin_code, delimiter)


def bacon2_e(text, bin_code=False, delimiter=" "):
    text = text.upper()
    return code_table_e(text, bacon1_table, {"a": "0", "b": "1"}, bin_code, delimiter)


def bacon2_d(text, bin_code=False, delimiter=" "):
    return code_table_d(text, bacon1_table, {"a": "0", "b": "1"}, bin_code, delimiter)


def chemical_symbol_convert(text, mode, delimiter=" "):
    if mode == '0':
        # Atomic number to sympol
        return code_table_e(text, chemical_symbol, {}, False, delimiter)
    elif mode == '1':
        # Symbol to atomic number
        return code_table_d(text, chemical_symbol, {}, False, delimiter)


def abc012(text, delimiter=" "):
    text = text.upper()
    return code_table_e(text, abc012_table, {}, False, delimiter)


def affine_e_a(text, a, b):
    if list_A.find(text) >= 0:
        list = list_A
    elif list_a.find(text) >= 0:
        list = list_a
    elif list_0.find(text) >= 0:
        list = list_0
    else:
        return text

    l = len(list)
    position = list.find(text)
    converted = (position*a + b) % l
    return "".join(list[converted])


def affine_d_a(text, a, b):
    if list_A.find(text) >= 0:
        list = list_A
    elif list_a.find(text) >= 0:
        list = list_a
    elif list_0.find(text) >= 0:
        list = list_0
    else:
        return text

    l = len(list)

    if a == 0:
        x = 0
    else:
        g, x, y = xgcd(a, l)
        if g != 1:
            return '#'

    position = list.find(text)
    converted = (position*x - b*x) % l
    return "".join(list[converted])


def affine_e(text, a, b):
    l = len(text)
    converted = ""
    for i in range(l):
        converted += affine_e_a(text[i], a, b)
    return converted


def affine_d(text, a, b):
    l = len(text)
    converted = ""
    for i in range(l):
        converted += affine_d_a(text[i], a, b)
    return converted


def text_split(text, step, sep=' '):
    result = ''
    for i in range(0, len(text), step):
        result += text[i:i+step] + sep
    result = result[:-1]
    return result


def table_subtitution(text, method):
    if method == 'A-a swap':
        t1 = list_A + list_a
        t2 = list_a + list_A
    elif method == 'Morse .- swap':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = '6789012345nj?wtqu?mbryiasxfkoeg?dpl?' + 'NJ?WTQU?MBRYIASXFKOEG?DPL?'
    elif method == 'Morse reverse':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = '9876543210nv?uelwhi?kfmaopyrstdbgxq?' + 'NV?UELWHI?KFMAOPYRSTDBGXQ?'
    elif method == 'Morse .- swap and reverse':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = '4321098765a?cgtyd?mvrqinsxlkoewjupfz' + 'A?CGTYD?MVRQINSXLKOEWJUPFZ'
    elif method == 'US keyboard left shift':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = '`123456789?vxswdfguhjknbio?earycqzt?0-p[]lm,.??VXSWDFGUHJKNBIO?EARYCQZT?'
    elif method == 'US keyboard right shift':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "234567890-snvfrghjokl;,mp[wtdyibecux=?]\?'./?1SNVFRGHJOKL;,MP[WTDYIBECUX"
    elif method == 'US keyboard right <-> left':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "0987654321;n,kijhgefdsvbwqpulyrmo.t/`????acxz-;N,KIJHGEFDSVBWQPULYRMO.T/"
    elif method == 'US keyboard up <-> down':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "zxcvbnm,..q53edrtykuio76l;afwgj4s2h1?????p890?Q53EDRTYKUIO76L;AFWGJ4S2H1"
    elif method == 'US keyboard to Dvorak keyboard':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "1234567890axje.uidchtnmbrl'poygk,qf;[]/=\swvz`AXJE.UIDCHTNMBRL'POYGK,QF;"
    elif method == 'Dvorak keyboard to US keyboard':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "1234567890anihdyujgcvpmlsrxo;kf.,bt/']-=\zwe[`ANIHDYUJGCVPMLSRXO;KF.,BT/"
    elif method == 'US keyboard to MALTRON keyboard':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "1234567890a,jiysfduthow>zlqcnbmgp>v<?????rk-x?A,JIYSFDUTHOW>ZLQCNBMGP>V<"
    elif method == 'MALTRON keyboard to US keyboard':
        t1 = '1234567890abcdefghijklmnopqrstuvwxyz-=[]\;,./`ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t2 = "1234567890atrh?gvkdc,puslwq;fjiym/eo>?????????ATRH?GVKDC,PUSLWQ;FJIYM/EO"

    return replace_all(text, t1, t2)


def phonetic_alphabet_e(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j.upper())
    return text


def phonetic_alphabet_d(text, dic):
    dic_swap = {v: k for k, v in dic.items()}
    for i, j in dic_swap.items():
        text = text.replace(i, j.upper())
    return text


def return_phonetic_alphabet_values(dic):
    text = 'Code table = ['
    for i in list_a:
        text += dic[i] + ' '

    text = text[:-1] + ']'
    return text


def letter_frequency(text, sortkey=0, reverse_flag=False):
    unique_text = unique(text)
    freq = []
    for letter in unique_text:
        freq.append([letter, text.count(letter)])
    return sorted(freq, key=lambda x: x[sortkey], reverse=reverse_flag)


def bigram_frequency(text):
    freq = []
    bigram = []
    for i in range(len(text)-1):
        if not ' ' in text[i:i+2]:
            bigram.append(text[i:i+2])

    unique_bigram = unique_list(bigram)
    for b in unique_bigram:
        freq.append([b, bigram.count(b)])
    return sorted(freq, key=lambda x: x[1], reverse=True)


def trigram_frequency(text):
    freq = []
    trigram = []
    for i in range(len(text)-1):
        if not ' ' in text[i:i+3]:
            trigram.append(text[i:i+3])

    unique_trigram = unique_list(trigram)
    for b in unique_trigram:
        freq.append([b, trigram.count(b)])
    return sorted(freq, key=lambda x: x[1], reverse=True)


def ngram_distance(text, ngram):
    import re
    if text == '' or ngram == '':
        return []
    ngram_length = len(ngram)
    iter = re.finditer(ngram, text)
    start_point_list = []
    for i in iter:
        start_point_list.append(i.span()[0])
    if len(start_point_list) == 0:
        return []

    distance = []
    for i in range(len(start_point_list)-1):
        distance.append(
            len(text[start_point_list[i]:start_point_list[i+1]].replace(' ', '')))

    unique_distance = unique_list(distance)
    freq = []
    for d in unique_distance:
        freq.append([d, distance.count(d)])
    return sorted(freq, key=lambda x: x[1], reverse=True)


def uu_encode(byte):
    result = ''.encode()
    for s in range(0, len(byte), 45):
        result += binascii.b2a_uu(byte[s:s+45])[:-1]
    return result


def uu_decode(text):
    result = ''.encode()
    for s in range(0, len(text), 60):
        result += binascii.a2b_uu(text[s:s+60])
    return result

# SECOM cipher
# http://users.telenet.be/d.rijmenants/en/secom.htm
# http://kryptografie.de/kryptografie/chiffre/secom.htm


def chain_addition(x):
    y = [0]*10
    for i in range(9):
        y[i] = (x[i]+x[i+1]) % 10
    y[9] = (x[9]+y[0]) % 10
    return y


def zero2ten(ls):
    return [10 if x == 0 else int(x) for x in ls]


def ten2zero(ls):
    return [0 if x == 10 else x for x in ls]


def make_key_digits(key):
    key = key.replace(" ", "").upper()
    if len(key) < 20:
        key = key*(int(20/len(key))+1)
    key_a = key[0:10]
    key_b = key[10:20]
    key_a_digits = ten2zero(assign_digits(key_a))
    key_b_digits = ten2zero(assign_digits(key_b))
    key_digits0 = [(x+y) % 10 for(x, y) in zip(key_a_digits, key_b_digits)]

    key_digits1 = chain_addition(key_digits0)
    key_digits2 = chain_addition(key_digits1)
    key_digits3 = chain_addition(key_digits2)
    key_digits4 = chain_addition(key_digits3)
    key_digits5 = chain_addition(key_digits4)
    key_digits = key_digits1+key_digits2+key_digits3+key_digits4+key_digits5

    return key_b_digits, key_digits


def make_checkerboard(key_digits):
    checkerboard_numbers = ten2zero(assign_digits(zero2ten(key_digits)))

    checkerboard = [0]*40
    checkerboard_index = [0]*40
    row0 = "ES TO NI A"
    row1 = "BCDFGHJKLM"
    row2 = "PQRUVWXYZ*"
    row3 = "1234567890"
    offset1 = int(checkerboard_numbers[2])-1
    offset2 = int(checkerboard_numbers[5])-1
    offset3 = int(checkerboard_numbers[8])-1

    for i in range(0, 10):
        checkerboard[i] = row0[i]
        checkerboard_index[i] = str(checkerboard_numbers[i])
    for i in range(0, 10):
        checkerboard[10+((i+offset1) % 10)] = row1[i]
        checkerboard_index[10+i] = str(checkerboard_numbers[2]) + \
            str(checkerboard_numbers[i])
    for i in range(0, 10):
        checkerboard[20+((i+offset2) % 10)] = row2[i]
        checkerboard_index[20+i] = str(checkerboard_numbers[5]) + \
            str(checkerboard_numbers[i])
    for i in range(0, 10):
        checkerboard[30+((i+offset3) % 10)] = row3[i]
        checkerboard_index[30+i] = str(checkerboard_numbers[8]) + \
            str(checkerboard_numbers[i])

    return checkerboard_numbers, checkerboard, checkerboard_index


def make_key_trans(key_digits, key_b_digits, checkerboard_numbers):
    key_trans_pre = [(x+y) % 10 for(x, y)
                     in zip(key_b_digits, checkerboard_numbers)]
    key_trans = columnar_e(key_digits, assign_digits(zero2ten(key_trans_pre)))

    first_trans_len = 0
    second_trans_len = 0
    already_encountered = []

    for i in range(1, 50):
        if second_trans_len > 9:
            break
        if not key_digits[-i] in already_encountered:
            if first_trans_len < 10:
                first_trans_len += key_digits[-i]
                already_encountered.append(key_digits[-i])
            else:
                second_trans_len += key_digits[-i]
                already_encountered.append(key_digits[-i])

    first_trans_key = key_trans[0:first_trans_len]
    second_trans_key = key_trans[first_trans_len:first_trans_len+second_trans_len]
    return first_trans_key, second_trans_key


def secom_e(c, key):
    #Checkerboard & keyの設定
    c = c.replace(" ", "*").upper()
    key_b_digits, key_digits = make_key_digits(key)
    checkerboard_numbers, checkerboard, checkerboard_index = make_checkerboard(
        key_digits[40:50])
    first_trans_key, second_trans_key = make_key_trans(
        key_digits, key_b_digits, checkerboard_numbers)

    # Chckerboard
    plain_numbers = ""
    for s in c:
        ind = checkerboard.index(s)
        c_ind = checkerboard_index[ind]
        plain_numbers += c_ind

    padding = "0" * (-len(plain_numbers) % 5)
    plain_numbers += padding

    # first columnar transosition
    numbers_trans1 = columnar_e(
        plain_numbers, assign_digits(zero2ten(first_trans_key)))

    # second disrupted columnar transposition
    numbers_trans2 = disrupted_columnar_e(
        numbers_trans1, assign_digits(zero2ten(second_trans_key)))

    return "".join(numbers_trans2)


def secom_d(c, key):
    #Checkerboard & keyの設定
    c = c.replace(" ", "").upper()
    key_b_digits, key_digits = make_key_digits(key)
    checkerboard_numbers, checkerboard, checkerboard_index = make_checkerboard(
        key_digits[40:50])
    first_trans_key, second_trans_key = make_key_trans(
        key_digits, key_b_digits, checkerboard_numbers)

    # second disrupted columnar transposition
    numbers_trans1 = disrupted_columnar_d(
        c, assign_digits(zero2ten(second_trans_key)))

    # first columnar transosition
    plain_numbers = columnar_d(
        numbers_trans1, assign_digits(zero2ten(first_trans_key)))

    # Chckerboard
    p = ""
    k = ""
    for i in range(len(plain_numbers)):
        k += plain_numbers[i]
        if (int(k) != checkerboard_numbers[2] and int(k) != checkerboard_numbers[5] and int(k) != checkerboard_numbers[8]):
            ind = checkerboard_index.index(k)
            p += checkerboard[ind]
            k = ""
        elif len(k) == 2:
            ind = checkerboard_index.index(k)
            p += checkerboard[ind]
            k = ""

    return "".join(p)


# end of definition. Below are used for test.
if __name__ == '__main__':
    #    print("")
    #    print(adfgvx_e("attack at 1200 AM", "na1c3h8tb2ome5wrpd4f6g7i9j0klqsuvxyz", "privacy"))
    #    print(adfgvx_d("DGDDDAGDDGAFADDFDADVDVFAADVX", "na1c3h8tb2ome5wrpd4f6g7i9j0klqsuvxyz", "privacy"))
    #    decode_help()
    #     print(bacon1_e("morse code", True))
    #    print(bacon1_d("01011 01101 10000 10001 00100 / 00010 01101 00011 00100 ", True))
    #     print(morse_d("00 000 101 111 1 / 0101 000 011 1 ",True))
    #    print(affine_e("Affine cipher 0123",5,8))
    #    print(beaufort("teststrings","beaufort"))
    #    print(bifid_d("UAEOLWRINS", "bgwkzqpndsioaxefclumthyvr"))
    #    print(polybius_d("52211533243324331543444423432444235214"))
    #    print(polybius_e("WFENININESTTHSITHWD"))
    #    print(kw(".*nest.*"))
    #    print(hexbash("01359ab"))
    pass
