from setup import access_modifiers as modifiers
from setup import property_words as prop
from setup import method_words as method
from setup import additional_start_words_for_class_members as prefix_class_members
from setup import additional_start_words_for_class as prefix_class
from setup import class_word
from setup import interface_word

# Comments Regex
comment_string = r"( *\*[^\n]*\n)"
comment_start = r"( *\/\*{2}\n)"
comment_end = r"(\s*\*\/\n)"
comment_regex = rf"({comment_start}{comment_string}*{comment_end})"

# Annotations Regex
annotation = r"( *@\w*\s?(\([^)]*\)\s)?)"


def list_to_regexp(words, char_after=''):
    return f'({f"{char_after}|".join(words)}{char_after})'


property_words_regex = list_to_regexp(prop)
method_words_regex = list_to_regexp(method)

# Regex
property_regex = f'({list_to_regexp(prefix_class_members," ")}?{list_to_regexp(modifiers, " ")}?{property_words_regex})'
method_regex = f'({list_to_regexp(prefix_class_members," ")}?{list_to_regexp(modifiers, " ")}?{method_words_regex})'
class_regex = f'({list_to_regexp(modifiers, " ")}?{list_to_regexp(prefix_class," ")}?({class_word}))'
interface_regex = f'({list_to_regexp(modifiers, " ")}?({interface_word}))'


# Result regex
def get_regex_for(member_regex):
    full_member_regex = r"( {0,4}" + member_regex + r' \w*(\((\n?["() \w@]*:\s?[\w?,<> *]+)*\s*\))?[^{=\n]*)'
    return f"(^{comment_regex}?{annotation}*{full_member_regex})"
