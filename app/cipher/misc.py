
def password_generate(length, table):
    import random
    table_length = len(table)

    result = ''
    for i in range(length):
        ind = random.randrange(0, table_length)
        result += table[ind]

    return result
