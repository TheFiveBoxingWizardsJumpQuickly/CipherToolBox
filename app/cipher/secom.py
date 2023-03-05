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
