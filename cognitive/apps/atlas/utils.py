
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
