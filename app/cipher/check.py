"""
TEST
"""
import sys


def assert_function(expected, result):
    print('Expected: ' + expected)
    print('Result  : ' + result)
    print(expected == result)


def test_purple1():
    # https://cryptocellar.org/pubs/purple-revealed.pdf
    # The 14-Part Message Decode
    # Added completement for missing character (i.e. -)
    import purple
    result = purple.purple_decode(
        text='ZTX ODNWKCCMAV NZ XYWEE TU QTCI MN VEU VIWB LUA XRR TL VA RG NTP CNO IUP JLC IVRTPJKAUH VMU DTH KTXYZE LQTVWG BUH FAW SHU LBF BH EXM YHF LOWDQKWHKK NX EBVPY HHG HEKXIOHQ HU H WIKYJYH PPFEAL NN AKIB OO ZN FRLQCFLJ TTSSDDOIOCVTW ZCKQ TSH XTIJCNWXOK UF NQR TTAOIH WTATWV',
        sixes_switch_position=9,
        twenties_switch_1_position=1,
        twenties_switch_2_position=24,
        twenties_switch_3_position=6,
        plugboard_full='NOKTYUXEQLHBRMPDICJASVWGZF',
        rotor_motion_key=231)
    expected = 'FOV TATAKIDASI NI MUIMI NO MOXI WO IRU BESI FYX XFC KZ ZR DX OOV BTN FYX FAE MEMORANDUM FIO FOV OOMOJI BAKARI FYX RAI CCY LFC BB CFC THE GOVERNMENT OF JAPAN LFL PROMPTED BY A GENUINE DESIRE TO COME TO AN AMICABLE UNDERSTANDING WITH THE GOVERNMENT OF THE UNITED STATES'

    print(sys._getframe().f_code.co_name)
    assert_function(expected, result)
    print('')


def test_purple2():
    # https://cryptocellar.org/pubs/purple-revealed.pdf
    # The 14-Part Message Encode
    # Added completement for missing character (i.e. -)
    import purple
    result = purple.purple_encode(
        text='FOV TATAKIDASI NI MUIMI NO MOXI WO IRU BESI FYX XFC KZ ZR DX OOV BTN FYX FAE MEMORANDUM FIO FOV OOMOJI BAKARI FYX RAI CCY LFC BB CFC THE GOVERNMENT OF JAPAN LFL PROMPTED BY A GENUINE DESIRE TO COME TO AN AMICABLE UNDERSTANDING WITH THE GOVERNMENT OF THE UNITED STATES',
        sixes_switch_position=9,
        twenties_switch_1_position=1,
        twenties_switch_2_position=24,
        twenties_switch_3_position=6,
        plugboard_full='NOKTYUXEQLHBRMPDICJASVWGZF',
        rotor_motion_key=231)
    expected = 'ZTX ODNWKCCMAV NZ XYWEE TU QTCI MN VEU VIWB LUA XRR TL VA RG NTP CNO IUP JLC IVRTPJKAUH VMU DTH KTXYZE LQTVWG BUH FAW SHU LBF BH EXM YHF LOWDQKWHKK NX EBVPY HHG HEKXIOHQ HU H WIKYJYH PPFEAL NN AKIB OO ZN FRLQCFLJ TTSSDDOIOCVTW ZCKQ TSH XTIJCNWXOK UF NQR TTAOIH WTATWV'

    print(sys._getframe().f_code.co_name)
    assert_function(expected, result)
    print('')


def test_enigma1():
    # http://anti.rosx.net/etc/tools/enc_enigma.php
    import enigma
    result = enigma.enigma(
        text='QBL TWLDAHH YEO EFPTWYB LENDP MKOX LDFAMUDWIJDXRJZ',
        rotor_left_id=1, rotor_mid_id=2, rotor_right_id=5,
        reflector_id='B', rotor_key='XWB', ringsetting_key='FVN', plugboard=['PO', 'ML', 'IU', 'KJ', 'NH', 'YT', 'GB', 'VF', 'RE', 'DC'])
    expected = 'DER FUEHRER IST TODXDER KAMPF GEHT WEITERXDOENITZX'

    print(sys._getframe().f_code.co_name)
    assert_function(expected, result)
    print('')


def test_enigma2():
    # http://investigate.ingress.com/2016/02/18/of-heaven-and-earth/ :daily passcode
    import enigma
    result = enigma.enigma(
        text='zuulpguxlkvjwmyrjbclxfoa',
        rotor_left_id=1, rotor_mid_id=2, rotor_right_id=3,
        reflector_id='B', rotor_key='AMT', ringsetting_key='AAA', plugboard=[])
    expected = 'NINEOSNFIVEMTHREEPSEVENX'

    print(sys._getframe().f_code.co_name)
    assert_function(expected, result)
    print('')


def test_enigma3():
    # https://plus.google.com/109846653838501599116/posts/PVJbMUDzhpa :VI Noir 'Enigma'
    import enigma
    result = enigma.enigma(
        text='QEVYRTCBIAAVGRRZIPGLUFWTTGBXZAZUJCEKFOGQGRDUMCPHWUFLVLIOAWFBWVWUODKQLN',
        rotor_left_id=4, rotor_mid_id=5, rotor_right_id=1,
        reflector_id='B', rotor_key='VIA', ringsetting_key='AAA', plugboard=['NO', 'IR'])
    expected = 'AXPUZZLEXINXTENXANDXONEXPARTSXXIMPORTANTXINTELXRUCGXZTFNINENOURISHTWOX'

    print(sys._getframe().f_code.co_name)
    assert_function(expected, result)
    print('')


def test_enigma4():
    # http://www.ancientsocieties.com/question-mark/ :ANCSOC 'QUESTION MARK'
    import enigma
    result = enigma.enigma(
        text='XWTYIHAWSOYJYQTDMTIFP',
        rotor_left_id=4, rotor_mid_id=5, rotor_right_id=1,
        reflector_id='B', rotor_key='YFD', ringsetting_key='XQO', plugboard=['MP', 'LX', 'YJ', 'SC', 'EW', 'AV', 'OZ', 'KR', 'NQ', 'TF'])
    expected = 'WAXCYLINDERPHONOGRAPH'

    print(sys._getframe().f_code.co_name)
    assert_function(expected, result)
    print('')


"""
test_purple1()
test_purple2()
"""
test_enigma1()
test_enigma2()
test_enigma3()
test_enigma4()
