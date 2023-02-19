def rev(c):
    return c[::-1]


def columnar_e(c, col):
    p = [0]*len(c)
    left_col_cnt = len(c) % len(col)
    row_cnt1 = int(len(c)/len(col))+1
    row_cnt2 = int(len(c)/len(col))

    i = 0
    for j in range(len(col)):
        ind = col.index(j+1)
        if ind < left_col_cnt:
            row_cnt = row_cnt1
        else:
            row_cnt = row_cnt2
        for k in range(row_cnt):
            p[i] = c[k*len(col)+ind]
            i += 1

    return p


def columnar_d(c, col):
    p = [0]*len(c)
    left_col_cnt = len(c) % len(col)
    row_cnt1 = int(len(c)/len(col))+1
    row_cnt2 = int(len(c)/len(col))

    i = 0
    for j in range(len(col)):
        ind = col.index(j+1)
        if ind < left_col_cnt:
            row_cnt = row_cnt1
        else:
            row_cnt = row_cnt2
        for k in range(row_cnt):
            p[k*len(col)+ind] = c[i]
            i += 1

    return p


def disrupted_columnar_e(c, col):
    rows_full = int(len(c)/len(col))
    lastrow_len = len(c) % len(col)

    trans_pre = [0]*len(c)
    ord_x = 0
    curr_len = len(col)
    cnt = 0
    for i in range(rows_full):
        if curr_len == len(col):
            ord_x += 1
            curr_len = col.index(ord_x)
        else:
            curr_len += 1
        for j in range(curr_len):
            trans_pre[i*len(col)+j] = c[cnt]
            cnt += 1

    if lastrow_len > 0:
        for j in range(lastrow_len):
            trans_pre[rows_full*len(col)+j] = c[cnt]
            cnt += 1

    ord_x = 0
    curr_len = len(col)
    for i in range(rows_full):
        if curr_len == len(col):
            ord_x += 1
            curr_len = col.index(ord_x)
        else:
            curr_len += 1
        for j in range(curr_len, len(col)):
            trans_pre[i*len(col)+j] = c[cnt]
            cnt += 1

    p = columnar_e(trans_pre, col)
    return p


def disrupted_columnar_d(c, col):
    rows_full = int(len(c)/len(col))
    lastrow_len = len(c) % len(col)
    trans_pre = columnar_d(c, col)

    p = [0]*len(c)
    ord_x = 0
    curr_len = len(col)
    cnt = 0
    for i in range(rows_full):
        if curr_len == len(col):
            ord_x += 1
            curr_len = col.index(ord_x)
        else:
            curr_len += 1
        for j in range(curr_len):
            p[cnt] = trans_pre[i*len(col)+j]
            cnt += 1

    if lastrow_len > 0:
        for j in range(lastrow_len):
            p[cnt] = trans_pre[rows_full*len(col)+j]
            cnt += 1

    ord_x = 0
    curr_len = len(col)
    for i in range(rows_full):
        if curr_len == len(col):
            ord_x += 1
            curr_len = col.index(ord_x)
        else:
            curr_len += 1
        for j in range(curr_len, len(col)):
            p[cnt] = trans_pre[i*len(col)+j]
            cnt += 1

    return p


def railfence_e(text, rails, offset=0):
    place = [["", 0] for i in range(len(text) + offset)]
    line_cycle = list(range(rails)) + list(range(rails-1)[:0:-1])
    for i in range(len(text)):
        place[i + offset] = [text[i], line_cycle[(i + offset) % (rails*2 - 2)]]

    result = ""
    for i in range(rails):
        for s in place:
            if s[1] == i:
                result += s[0]
    return result


def railfence_d(text, rails, offset=0):
    place = [["", 0] for i in range(len(text) + offset)]
    line_cycle = list(range(rails)) + list(range(rails-1)[:0:-1])
    for i in range(len(text)):
        place[i + offset] = ["", line_cycle[(i + offset) % (rails*2 - 2)]]

    t = 0
    for i in range(rails):
        for j in range(len(text)):
            if place[j + offset][1] == i:
                place[j + offset][0] = text[t]
                t += 1

    result = ""
    for s in place:
        result += s[0]
    return result


def rect(text, col):
    return [text[i:i+col] for i in range(0, len(text), col)]


def rect_reverse_even(text, col):
    fill_count = -len(text) % col
    text = text + ' ' * fill_count

    direction = 1
    result = []
    for i in range(0, len(text), col):
        result.append(text[i:i+col][::direction])
        direction *= -1
    return result


def periodic_transposition_e(text, key):
    result = ''
    text_length = len(text)
    key_length = len(key)
    for i in range(0, text_length, key_length):
        r = text[i:i+key_length]
        for j in range(key_length):
            if key[j] <= len(r):
                result += r[key[j]-1]
    return result


def periodic_transposition_d(text, key):
    result = ''
    text_length = len(text)
    key_length = len(key)

    key_reverse = [0]*key_length
    for i in range(key_length):
        key_reverse[key[i]-1] = i+1

    for i in range(0, text_length, key_length):
        r = text[i:i+key_length]
        if len(r) == key_length:
            for j in range(key_length):
                result += r[key_reverse[j]-1]
        else:
            key2 = []
            for k in range(key_length):
                if key[k] <= len(r):
                    key2.append(key[k])
            key_reverse2 = [0]*key_length
            for i in range(len(r)):
                key_reverse2[key2[i]-1] = i+1
            for j in range(len(r)):
                result += r[key_reverse2[j]-1]
    return result


def swap_xy_axes(text):
    a = text.split('\n')
    max_y = len(a)
    max_x = 1
    for r in a:
        max_x = max(max_x, len(r))

    a2 = []
    for r in a:
        a2.append(r + ' '*(max_x - len(r)))

    b = []

    for x in range(max_x):
        c = ''
        for y in range(max_y):
            c += a2[y][x]
        b.append(c)

    return '\n'.join(b)


def skip_e(text, step):
    step = int(step)
    order = []
    position = 0
    l = len(text)
    for i in range(l):
        if position in order:
            position += 1
        order.append(position)
        position = (position + step) % l

    result = ''.join([text[i] for i in order])
    return result


def skip_d(text, step):
    step = int(step)
    order = []
    position = 0
    l = len(text)
    for i in range(l):
        if position in order:
            position += 1
        order.append(position)
        position = (position + step) % l

    reverse_order = [0]*l
    for i in range(l):
        reverse_order[order[i]] = i

    result = ''.join([text[i] for i in reverse_order])
    return result
