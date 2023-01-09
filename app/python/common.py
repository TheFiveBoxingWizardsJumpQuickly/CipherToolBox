import re

def assign_digits(x):
    a=[0]*len(x)

    for i in range(len(x)):
        a[i]=[x[i],i]
        
    a.sort(key=lambda t:(t[0],t[1]))

    b=[0]*len(x)
    for i in range(len(x)):
        b[i]=a[i][1]
        
    c=[0]*len(x)
    for i in range(len(x)):
        c[b[i]]=i+1

    return c

def mixed_alphabet(keyword, combined=False):
    kw_alphabet_added = keyword.upper() + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if combined:
        kw_alphabet_added = kw_alphabet_added.replace("J","I")

    already_appeared=[]
    result =""
    for s in kw_alphabet_added:
        if not s in already_appeared:
            result+=s
            already_appeared.append(s)
    return result

def unique(text, sort=False):
    already_appeared=[]
    for s in text:
        if not s in already_appeared:
            already_appeared.append(s)
    if sort:
        already_appeared.sort()
    result = ''.join(already_appeared)
    return result

def unique_list(list, sort=False):
    already_appeared=[]
    for s in list:
        if not s in already_appeared:
            already_appeared.append(s)
    if sort:
        already_appeared.sort()
    
    return already_appeared

def mixed_alphanumeric(keyword):
    kw_alphabet_added = keyword.upper() + "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return unique(kw_alphabet_added)

def replace_all_words(text, dic):
    #this may be fast, but if the words after conversion is included in the map_from table, duplicatedly affected and get wrong. 
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def replace_all(text, table_from, table_to):
    result =''
    for s in text:
        if s in table_from:
            result += table_to[table_from.find(s)]
        else:
            result += s
    return result

def replace_all_case_insensitive(text, table_from, table_to):
    result =''
    table_from_lower = table_from.lower()
    table_from_upper = table_from.upper()
    table_to_lower = table_to.lower()
    table_to_upper = table_to.upper()

    for s in text:
        if s in table_from_lower:
            result += table_to_lower[table_from_lower.find(s)]
        elif s in table_from_upper:
            result += table_to_upper[table_from_upper.find(s)]
        else:
            result += s
    return result

def split_by_len(text, length):
    return [text[i:i+length] for i in range(0,len(text),length)]

def extract_integer_only(text):
    import re
    return re.sub('\\D', '', text)

def characters_validation(text, encoding_method):
    if encoding_method == 'base16':
        return re.match(r'^[A-Fa-f0-9]+$', text) is not None
    elif encoding_method == 'base32':
        return re.match(r'^[A-Z2-7=]+$', text) is not None
    elif encoding_method == 'base64':
        return re.match(r'^[A-Za-z0-9+=]+$', text) is not None
    elif encoding_method == 'uuencode':
        return re.match(r'^[`-_]+$', text) is not None
    elif encoding_method == 'ascii85':
        return re.match(r'^[0-9a-zA-Z!#$%&()*+-;<=>?@^_`{|}]+$', text) is not None
    else:
        return False


