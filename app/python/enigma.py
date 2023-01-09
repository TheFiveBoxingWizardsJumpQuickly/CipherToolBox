# Static
abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

rotor_number_i = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 0]
rotor_number_ii = ['AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E', 0, 0]
rotor_number_iii = ['BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V', 0, 0]
rotor_number_iv = ['ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J', 0, 0]
rotor_number_v = ['VZBRGITYUPSDNHLXAWMJQOFECK', 'Z', 0, 0]
reflector_a = 'EJMZALYXVBWFCRQUONTSPIKHGD'
reflector_b = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
reflector_c = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'

std_r = {1: rotor_number_i, 2: rotor_number_ii,
         3: rotor_number_iii, 4: rotor_number_iv, 5: rotor_number_v}
std_f = {'A': reflector_a, 'B': reflector_b, 'C': reflector_c}


# Utility functions
def rot(c, offset):
    return abc[(abc.find(c) + offset) % len(abc)]


def swap(text, plug):
    return text.translate(str.maketrans(plug, plug[::-1]))


def notch(rotor_left, rotor_right):
    return abc[(rotor_left[2]-1) % len(abc)] == rotor_left[1] or abc[(rotor_right[2]) % len(abc)] == rotor_right[1]


def shift_rotor(rotor):
    return [rotor[0][1:]+rotor[0][0], rotor[1], (rotor[2]+1) % len(rotor[0]), rotor[3]]


def shift_rotor_n(rotor, n):
    x = rotor
    for i in range(n):
        x = shift_rotor(x)
    return x


def incr_rotors(rotors):
    incremented_rotors = rotors
    incremented_rotors[0] = shift_rotor(incremented_rotors[0])
    if(notch(incremented_rotors[0], incremented_rotors[1])):
        incremented_rotors[1] = shift_rotor(incremented_rotors[1])
        if(notch(incremented_rotors[1], incremented_rotors[2])):
            incremented_rotors[2] = shift_rotor(incremented_rotors[2])
    return incremented_rotors


def shift_ring(ring):
    return ring[-1]+ring[0:-1]


def shift_ring_n(ring, n):
    x = ring
    for i in range(n):
        x = shift_ring(x)
    return x

# Enigma machine emulation


def enigma(text, rotor_left_id, rotor_mid_id, rotor_right_id, reflector_id, rotor_key, ringsetting_key, plugboard):

    rotors = [std_r[rotor_right_id], std_r[rotor_mid_id], std_r[rotor_left_id]]
    reflector = std_f[reflector_id]
    rotor_key = rotor_key[::-1].upper()
    ringsetting_key = ringsetting_key[::-1].upper()

    rotors = [shift_rotor_n(rotors[i], abc.find(rotor_key[i]))
              for i in range(len(rotors))]
    rotors = [[rotors[i][0], rotors[i][1], rotors[i][2], abc.find(
        ringsetting_key[i])] for i in range(len(rotors))]

    text = text.upper()

    for plug in plugboard:
        text = swap(text, plug)

    result = ''

    for counter in range(len(text)):
        t = text[counter]
        if ord(t) < ord('A') or ord('Z') < ord(t):
            result += t
        else:
            rotors = incr_rotors(rotors)

            for rotor in rotors:
                t = rot(t, -rotor[3])
                t = rotor[0][abc.find(t)]
                t = rot(t, -rotor[2])
                t = rot(t, rotor[3])

            # this line is the only difference between encoding and decoding
            t = reflector[abc.find(t)]

            for rotor in rotors[::-1]:
                t = rot(t, -rotor[3])
                t = rot(t, rotor[2])
                t = abc[rotor[0].find(t)]
                t = rot(t, rotor[3])

            result += t

    for plug in plugboard:
        result = swap(result, plug)

    return result


def plugboard_gen(txt):
    import re
    txt = re.sub(r"[^a-zA-Z_]", "", txt).upper()

    unique_txt = ""
    already_appeared = []
    for s in txt:
        if not s in already_appeared:
            unique_txt += s
            already_appeared.append(s)

    result = []

    even_flag = True
    for s in unique_txt:
        even_flag = not even_flag
        if even_flag:
            result.append(w+s)
        else:
            w = s

    return result
