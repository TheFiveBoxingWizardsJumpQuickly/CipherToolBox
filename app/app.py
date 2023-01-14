import os
import re
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
from app.python.fn import *

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon.ico', )


@app.route('/<string:file>')
def show_page(file):
    file = file.split('.')[0]
    return render_template(file+'.html', BASEURL=request.base_url)


@app.route('/fn/rot', methods=['post'])
def fn_rot():
    input_text = request.json['input_text']

    results = {}
    for i in range(26):
        results[i] = str(i).zfill(2) + ': ' + rot(input_text, i)
    return results


@app.route('/fn/vigenere', methods=['post'])
def fn_vigenere():
    input_text = request.json['input_text']
    key = request.json['key']
    results = {}
    results[0] = 'Text: ' + input_text
    results[1] = 'Key: ' + key
    results[2] = 'Decoded: ' + vig_d(input_text, key)
    results[3] = 'Encoded: ' + vig_e(input_text, key)
    results[4] = 'Beaufort: ' + beaufort(input_text, key)
    results[5] = 'Auto key Decoded: ' + vig_d_auto(input_text, key)
    results[6] = 'Auto key Encoded: ' + vig_e_auto(input_text, key)
    return results


@app.route('/fn/enigma', methods=['post'])
def fn_enigma():
    input_text = request.json['input_text']
    left_rotor = request.json['left_rotor']
    mid_rotor = request.json['mid_rotor']
    right_rotor = request.json['right_rotor']
    reflector = request.json['reflector']
    rotor_key = request.json['rotor_key']
    ring_key = request.json['ring_key']
    plug_board = request.json['plug_board']

    input_text = input_text.upper()
    rotor_key = re.sub(r"[^a-zA-Z]", "", rotor_key).upper().ljust(3, 'A')
    ring_key = re.sub(r"[^a-zA-Z]", "", ring_key).upper().ljust(3, 'A')
    plug_board = plugboard_gen(plug_board)

    results = {}
    results[0] = 'Text: ' + input_text
    results[1] = 'Rotor Set: ' + left_rotor + \
        ' ' + mid_rotor + ' ' + right_rotor
    results[2] = 'Reflector: ' + reflector
    results[3] = 'Rotator key: ' + rotor_key
    results[4] = 'Ring Setting Key: ' + ring_key
    results[5] = 'Plug Board: ' + ','.join(plug_board)
    results[6] = '------'
    results[7] = 'Enigma output: ' + enigma(text=input_text,
                                            rotor_left_id=int(left_rotor),
                                            rotor_mid_id=int(mid_rotor),
                                            rotor_right_id=int(right_rotor),
                                            reflector_id=reflector,
                                            rotor_key=rotor_key,
                                            ringsetting_key=ring_key,
                                            plugboard=plug_board)
    return results


@app.route('/fn/purple', methods=['post'])
def fn_purple():
    input_text = request.json['input_text']
    sixes_switch_position = int(request.json['sixes_switch_position'])
    twenties_switch_1_position = int(
        request.json['twenties_switch_1_position'])
    twenties_switch_2_position = int(
        request.json['twenties_switch_2_position'])
    twenties_switch_3_position = int(
        request.json['twenties_switch_3_position'])
    plugboard_full = request.json['plugboard_full']
    rotor_motion_key = int(request.json['rotor_motion_key'])

    input_text = input_text.upper()
    plugboard_full = re.sub(
        r"[^a-zA-Z]", "", plugboard_full).upper()

    results = {}
    results[0] = 'Text: ' + input_text
    results[1] = 'Rotor Position: SIXes= ' + str(sixes_switch_position) + \
        ' TWENTIES_1= ' + str(twenties_switch_1_position) + \
        ' TWENTIES_2= ' + str(twenties_switch_2_position) + \
        ' TWENTIES_3= ' + str(twenties_switch_3_position)
    results[2] = 'Motion: ' + str(rotor_motion_key)
    results[3] = 'Plug Board: ' + plugboard_full
    results[4] = '------'
    results[5] = 'PURPLE Decode: ' + purple_decode(text=input_text,
                                                   sixes_switch_position=sixes_switch_position,
                                                   twenties_switch_1_position=twenties_switch_1_position,
                                                   twenties_switch_2_position=twenties_switch_2_position,
                                                   twenties_switch_3_position=twenties_switch_3_position,
                                                   plugboard_full=plugboard_full,
                                                   rotor_motion_key=rotor_motion_key
                                                   )
    results[6] = '------'
    results[7] = 'PURPLE Encode: ' + purple_encode(text=input_text,
                                                   sixes_switch_position=sixes_switch_position,
                                                   twenties_switch_1_position=twenties_switch_1_position,
                                                   twenties_switch_2_position=twenties_switch_2_position,
                                                   twenties_switch_3_position=twenties_switch_3_position,
                                                   plugboard_full=plugboard_full,
                                                   rotor_motion_key=rotor_motion_key
                                                   )
    return results


@app.route('/fn/prime', methods=['post'])
def fn_prime():
    input_text = request.json['input_text']

    factor, notation = factorize(extract_integer_only(input_text))
    results = {}
    results[0] = factor
    results[1] = notation
    return results


@app.route('/fn/pwgen', methods=['post'])
def fn_pwgen():
    char_type = request.json['char_type']
    length = request.json['length']

    list_symbol = '!@#$%^&'

    map = {
        '0': list_A + list_a + list_0,
        '1': list_A + list_a + list_0 + list_symbol,
        '2': list_A + list_a,
        '3': list_A,
        '4': list_a,
        '5': list_0,
        '6': list_A + list_a + list_symbol,
        '7': list_A + list_0,
        '8': list_a + list_0
    }
    table = map.get(char_type)

    results = {}
    results[0] = password_generate(int(length), table)
    return results


@app.route('/fn/charcode', methods=['post'])
def fn_charcode():
    input_text = request.json['input_text']
    base = int(request.json['base'])
    mode = request.json['mode']

    results = {}
    if base < 2 or 36 < base:
        results[0] = 'Number base should be between 2-36.'
    else:
        if mode == 'Char to Codepoint':
            results[0] = 'UTF-8: ' + \
                ' '.join([char_to_codepoint(char, codec='utf_8', base=base)
                          for char in input_text])
            results[1] = 'Shift JIS: ' + \
                ' '.join([char_to_codepoint(char, codec='shift_jis', base=base)
                          for char in input_text])
            results[2] = 'EUC JP: ' +\
                ' '.join([char_to_codepoint(char, codec='euc_jp', base=base)
                          for char in input_text])
            results[3] = 'ISO-2022-JP: ' +\
                ' '.join([char_to_codepoint(char, codec='iso2022_jp', base=base)
                          for char in input_text])
        elif mode == 'Codepoint to Char':
            valid_chars = set(' ' + valid_chars_for_base_n(base))
            if not all(c in valid_chars for c in input_text):
                results[0] = 'Input contains invalid characters for base ' + \
                    str(base)
            else:
                code_points = list(
                    filter(lambda x: len(x) > 0, input_text.split(' ')))
                results[0] = 'UTF-8: ' + \
                    ''.join([codepoint_to_char(code_point, codec='utf_8', base=base)
                            for code_point in code_points])
                results[1] = 'Shift JIS: ' + \
                    ''.join([codepoint_to_char(code_point, codec='shift_jis', base=base)
                            for code_point in code_points])
                results[2] = 'EUC JP: ' +\
                    ''.join([codepoint_to_char(code_point, codec='euc_jp', base=base)
                            for code_point in code_points])
                results[3] = 'ISO-2022-JP: ' +\
                    ''.join([codepoint_to_char(code_point, codec='iso2022_jp', base=base)
                            for code_point in code_points])

    return results


@app.route('/fn/base64', methods=['post'])
def fn_base64():
    input_text = request.json['input_text']
    mode = request.json['mode']

    results = {}
    if mode == 'Decode':
        # Base32 block
        results[0] = '---Base32---'
        input_text_formatted = input_text.upper()
        input_text_formatted = input_text_formatted + \
            "="*(-len(input_text_formatted) % 8)
        try:
            results[2] = 'decoded: ' + \
                base64.b32decode(input_text_formatted).decode()
        except:
            results[2] = '# input was not interpreted as Base32 encoding.'
        results[3] = ''

        # Base64 block
        results[4] = '---Base64---'
        input_text_formatted = input_text + "="*(-len(input_text) % 4)
        try:
            results[6] = 'decoded: ' + \
                base64.b64decode(
                    input_text_formatted, validate=True).decode()
        except:
            results[6] = '# input was not interpreted as Base64 encoding.'
        results[7] = ''

        # UUencoding block
        results[8] = '---UUencode---'
        input_text_formatted = input_text + " "*(-len(input_text) % 4)
        try:
            results[10] = 'decoded: ' + \
                uu_decode(input_text_formatted).decode()
        except:
            results[10] = '# input was not interpreted as UU encoding.'
        results[11] = ''

        # ASCII85 block
        results[12] = '---ASCII85---'
        input_text_formatted = input_text
        try:
            results[14] = 'decoded: ' + \
                base64.a85decode(input_text_formatted).decode()
        except:
            results[14] = '# input was not interpreted as ASCII85 encoding.'
        results[15] = ''

        # Base85 block
        results[16] = '---Base85---'
        input_text_formatted = input_text
        try:
            results[18] = 'decoded: ' + \
                base64.b85decode(input_text_formatted).decode()
        except:
            results[18] = '# input was not interpreted as BASE85 encoding.'
        results[19] = ''

    elif mode == 'Encode':
        results[0] = 'Base32:'
        results[1] = str(base64.b32encode(input_text.encode()))[2:-1]
        results[2] = ''
        results[3] = 'Base64:'
        results[4] = str(base64.b64encode(input_text.encode()))[2:-1]
        results[5] = ''
        results[6] = 'UUencode:'
        results[7] = str(uu_encode(input_text.encode()))[2:-1]
        results[8] = ''
        results[9] = 'ASCII85:'
        results[10] = str(base64.a85encode(input_text.encode()))[2:-1]
        results[11] = ''
        results[12] = 'Base85:'
        results[13] = str(base64.b85encode(input_text.encode()))[2:-1]

    return results


@app.route('/fn/rectangle', methods=['post'])
def fn_rectangle():
    input_text = request.json['input_text']
    mode = request.json['mode']

    results = {}

    t = 0

    results[t] = 'Text length = ' + str(len(input_text))
    t += 1
    for i in range(2, math.ceil(len(input_text)/2)+1):
        if len(input_text) % i == 0 or mode == 'All pattern':
            rectangle_i = rect(input_text, i)

            results[t] = '-----'
            t += 1

            results[t] = 'Column count = ' + str(i)
            t += 1
            for r in range(len(rectangle_i)):
                results[t] = rectangle_i[r]
                t += 1

    return results
