
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

def color_by_relation(relation_name):
    '''color_by_relation returns node color based on relation type
    :param relation_name: the name of the relation to look up color for
    '''
    colors = {"ASSERTS":"#3C7263", # task --asserts--> concept
              "MEASUREDBY": "#D89013", # concept --measuredby--> contrast
              "DERIVEDFROM": "#63506D", # task --derivedfrom--> task
              "HASCONDITION":"#BC1079", # contrast --hascondition--> condition
              "HASCONTRAST": "#D89013", # condition --hascontrast--> contrast
              "PARTOF":"#3C7263",  # concept
              "KINDOF":"#3C7263"}  # concept

    if relation_name in colors:
        return colors[relation_name]
    return "#FFFFFF"
