from pathlib import Path
from regex import *
from extractor import *
from setup import *
from param import Param
from docx.table import Table
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt


class Method:

    __comment_params = {}

    def __init__(self, method_code: string):
        self.comment = ""
        self.params = []
        self.result = ""
        self.type = ""
        self.name = ""
        self.access_modifier = ""
        self.__extract_name(method_code)
        self.__extract_type(method_code)
        self.__extract_access_modifier(method_code)
        self.__extract_params_from_signature(method_code)
        self.__extract_comment(method_code)

    def __extract_name(self, method_code: string):
        regex = rf'{method_words_regex} [\w\d]+'
        matches = re.search(regex, method_code)
        if matches:
            self.name = matches.group().split(' ')[-1]
        else:
            raise Exception("Incorrect file. Cannot extract method name")

    def __extract_access_modifier(self, method_code: string):
        match = re.search(method_regex, method_code)
        modifiers_regex = list_to_regexp(access_modifiers)
        match = re.search(modifiers_regex, match.group())
        if match:
            self.access_modifier = match.group()
        else:
            self.access_modifier = "public"

    def __extract_type(self, method_code: string):
        matches = re.search(r'\)\s?:\s?[\w\d<, >*?]+', method_code)
        if matches:
            self.type = matches.group().split(':')[-1].strip()
        else:
            self.type = implicit_type_warning

    def __extract_comment(self, method_code: string):
        matches = re.search(comment_regex, method_code, re.MULTILINE)
        if matches:
            self.comment = extract_comment(matches.group())
            self.result = extract_return(matches.group())
            self.__comment_params = extract_params(matches.group())

    def __extract_params_from_signature(self, method_code: string):
        matches = re.findall(r'[\w\d]+\s?:\s?[\w\d<, >?*]+', method_code)
        for strParam in matches:
            name = strParam.split(":")[0].strip().split()[-1]
            param = Param(name)
            param.type = strParam.split(":")[-1].strip()
            if self.comment.__contains__(name):
                param.comment = self.__comment_params[name]
            self.params.append(param)

    def __params_to_str(self):
        res_str = ""
        for param in self.params:
            res_str += f'{param.name}: {param.type}'
            if param.comment:
                res_str += f' - {param.comment}'
            res_str += ';\n'
        if res_str:
            return res_str
        return "-"

    def __get_comment(self):
        res_str = self.comment
        if self.result:
            res_str += f'\n{self.result}'
        return res_str

    def method_to_row(self, table: Table):
        cells = table.add_row().cells
        cells[0].text = self.name
        cells[1].text = self.access_modifier
        cells[2].text = self.type
        cells[3].text = self.__params_to_str()
        cells[4].text = self.__get_comment()
        for i in range(5):
            cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
            cells[i].paragraphs[0].runs[0].font.size = Pt(12)
