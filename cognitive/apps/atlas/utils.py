
def clean_html(html,replacements=None):
    '''clean_html will replace newlines with <br> for rendering, along with \r characters
    :param html: the html to clean
    :param replacements: additional list of paired lists eg [["string","replace"]...] (optional)
    '''
    replace_sets = [["\n","<br>"],["\r",""]]

    if replacements != None:
        replace_sets = replace_sets + replacements
    
    for replace_set in replace_sets:
        text = replace_set[0]
        replacement = replace_set[1]
        html = html.replace(text,replacement)
    return html


def update_lookup(lookup,key,entry):
    '''update_lookup will update a lookup dictionary with an entry. If the key exists, the entry is appended to 
    the existing list. if not, it is added.
    :param lookup: dictionary to update
    :param entry: the entry to add to the list
    '''
    if key in lookup:
        lookup[key].append(entry)
    else:
        lookup[key] = [entry]
    return lookup

