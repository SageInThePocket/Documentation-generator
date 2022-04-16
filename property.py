import re
import string
from regex import *
from extractor import *
from setup import *
from setup import explicit_type_warning
from docx.table import Table
from docx.shared import Pt


class Property:

    def __init__(self, property_code: string):
        self.comment = ""
        self.result = ""
        self.type = ""
        self.name = ""
        self.access_modifier = ""
        self.__extract_comment(property_code)
        self.__extract_name(property_code)
        self.__extract_type(property_code)
        self.__extract_access_modifier(property_code)

    def __extract_name(self, property_code: string):
        regex = rf'{property_words_regex} [\w\d]+'
        matches = re.search(regex, property_code)
        if matches:
            self.name = matches.group().split(' ')[-1]
        else:
            raise Exception("Incorrect file. Cannot extract property name")

    def __extract_access_modifier(self, property_code: string):
        match = re.search(property_regex, property_code)
        modifiers_regex = list_to_regexp(access_modifiers)
        match = re.search(modifiers_regex, match.group())
        if match:
            self.access_modifier = match.group()
        else:
            self.access_modifier = "public"

    def __extract_comment(self, property_code: string):
        matches = re.search(comment_regex, property_code, re.MULTILINE)
        if matches:
            self.comment = extract_comment(matches.group())
            self.result = extract_return(matches.group())

    def __extract_type(self, property_code: string):
        m = re.search(rf'{property_words_regex} [\w\d]*\s*:\s?[\w\d]*(<([\w\d ]*,?)+>)?', property_code)
        if m:
            self.type = m.group().split(':')[-1].strip()
        else:
            self.type = explicit_type_warning

    def __get_comment(self):
        res_str = self.comment
        if self.result:
            res_str += f'\n{self.result}'
        return res_str

    def to_row(self, table: Table):
        cells = table.add_row().cells
        cells[0].text = self.name
        cells[1].text = self.access_modifier
        cells[2].text = self.type
        cells[3].text = self.__get_comment()
        for i in range(4):
            cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
            cells[i].paragraphs[0].runs[0].font.size = Pt(12)
