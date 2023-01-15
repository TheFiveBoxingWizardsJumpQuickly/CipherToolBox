

def st1(Deck):
    ind = Deck.index('A')
    newDeck =[]
    if ind == 53:
        for i in range(54):
            if i == 0:
                newDeck.append(Deck[i])
            elif i == 1:
                newDeck.append(Deck[ind])
            else:
                newDeck.append(Deck[i-1])
    else:
        for i in range(54):
            if i == ind:
                newDeck.append(Deck[ind+1])
            elif i == ind + 1:
                newDeck.append(Deck[ind])
            else:
                newDeck.append(Deck[i])
    return newDeck

def st2(Deck):
    ind = Deck.index('B')
    newDeck =[]
    if ind == 53:
        for i in range(54):
            if i == 0 or i == 1:
                newDeck.append(Deck[i])
            elif i == 2:
                newDeck.append(Deck[ind])
            else:
                newDeck.append(Deck[i-1])
    elif ind == 52:
        for i in range(54):
            if i == 0 or i == 53:
                newDeck.append(Deck[i])
            elif i == 1:
                newDeck.append(Deck[ind])
            else:
                newDeck.append(Deck[i-1])
    else:
        for i in range(54):
            if i == ind:
                newDeck.append(Deck[ind+1])
            elif i == ind + 1:
                newDeck.append(Deck[ind+2])
            elif i == ind + 2:
                newDeck.append(Deck[ind])
            else:
                newDeck.append(Deck[i])
    return newDeck

def st3(Deck):
    ind_a = Deck.index('A')
    ind_b = Deck.index('B')
    ind_min = min(ind_a, ind_b)
    ind_max = max(ind_a, ind_b)
    cut_1 = Deck[0:ind_min]
    cut_2 = Deck[ind_min:ind_max+1]
    cut_3 = Deck[ind_max+1:]
    return cut_3 + cut_2 + cut_1

def st4(Deck):
    ind = Deck[53]
    cut_1 = Deck[0:ind]
    cut_2 = Deck[ind:53]
    cut_3 = Deck[53:]
    return cut_2 + cut_1 + cut_3

def st5(Deck, num):
    ind = num
    cut_1 = Deck[0:ind]
    cut_2 = Deck[ind:53]
    cut_3 = Deck[53:]
    return cut_2 + cut_1 + cut_3

def output_key(Deck):
    ind = Deck[0]
    if ind == 'A' or ind =='B':
        ind_num = 53
    else:
        ind_num = ind
    
    key = Deck[ind_num]
    if key == 'A' or key == 'B':
        key_num = 53
    else:
        key_num = key

    return key

def key_deck(Deck, phrase_num):
    phrase_length = len(phrase_num)
    for i in range(phrase_length):
        Deck = st1(Deck)
        Deck = st2(Deck)
        Deck = st3(Deck)
        Deck = st4(Deck)
        Deck = st5(Deck, phrase_num[i])
    return Deck


def generate_key(Deck, stream_length):
    key_stream = []
    for i in range(stream_length):
        Deck = st1(Deck)
        Deck = st2(Deck)
        Deck = st3(Deck)
        Deck = st4(Deck)
        key_stream.append(output_key(Deck))
    print(key_stream)

Deck = [40,1,41,2,42,3,43,4,44,5,45,6,46,7,47,8,48,9,49,
        10,50,11,51,12,52,13,27,14,28,15,29,16,30,17,31,
        18,32,19,33,20,34,21,35,22,36,23,37,24,38,25,39,26,'A','B']
phrase=[13,25,22,5,18,25,15,23,14,18,5,3,9,16,5,2,15,15,11]

Deck = key_deck(Deck, phrase)
print(Deck)
generate_key(Deck,10)
'''
if __name__ == "__main__":
    print('Test')
'''