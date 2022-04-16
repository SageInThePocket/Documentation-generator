import re
import string


def extract_comment(comment: string):
    matches = re.search(r'\*(\s?[^\n@]*\n)*', comment, re.MULTILINE)
    word_list = list(filter(None, re.split(r'[*\s]', matches.group())))
    return " ".join(word_list).strip('/').strip()


def extract_params(comment: string):
    matches = re.findall(r'@param \w+ [^@]*\n', comment, re.MULTILINE)
    name_to_description = {}
    for param in matches:
        word_list = list(filter(None, re.split(r'[*\s]', param)))
        param_name = word_list[1]
        param_desc = " ".join(word_list[2:])
        name_to_description[param_name] = param_desc
    return name_to_description


def extract_return(comment: string):
    matches = re.search(r'@return [^/]*', comment)
    if not matches:
        return ""
    word_list = list(filter(None, re.split(r'[*\s]', matches.group())))
    return " ".join(word_list[1:])