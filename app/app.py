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
