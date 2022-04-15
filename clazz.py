from pathlib import Path
from regex import *
from extractor import *
from setup import class_word
from docx.table import Table
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def _create_table(doc: Document, headers: [], name: string):
    p = doc.add_paragraph(name)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    p.runs[0].font.name = 'Times New Roman'
    table = doc.add_table(1, len(headers))
    table.style = 'Table Grid'
    table.autofit = True
    head_cells = table.rows[0].cells
    for i, item in enumerate(headers):
        p = head_cells[i].paragraphs[0]
        p.add_run(item).bold = True
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.runs[0].font.name = 'Times New Roman'
    return table

class Class:

    def __init__(self, class_code: string):
        self.comment = ""
        self.name = ""
        self.methods = []
        self.params = {}
        self.properties = []
        self.__extract_class_info(class_code)

    def __extract_class_info(self, code: string):
        self.__extract_class_name(code)
        self.__extract_comment(code)

    def __extract_class_name(self, info: string):
        regex = rf'{class_word} [\w\d]*(<([\w\d ]*,?)+>)?'
        matches = re.search(regex, info)
        if matches:
            self.name = matches.group().replace(class_word, "").strip()
            print(f'{info} -> {self.name}')
        else:
            raise Exception("Incorrect file. Cannot extract class name")

    def __extract_comment(self, info: string):
        matches = re.search(comment_regex, info, re.MULTILINE)
        if matches:
            self.comment = extract_comment(matches.group())
            self.params = extract_params(matches.group())

    def class_to_row(self, table: Table):
        cells = table.add_row().cells
        cells[0].text = self.name
        cells[1].text = self.comment
        for i in range(2):
            cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'

    def class_to_table(self, doc: Document()):
        if len(self.methods) > 0 or len(self.properties) > 0:
            doc.add_paragraph()
            p = doc.add_paragraph(f'Описание свойств и методов класса {self.name}.kt')
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            p.runs[0].font.name = 'Times New Roman'

            if len(self.methods) > 0:
                headers = ['Имя', 'Модификатор доступа', "Тип", "Параметры", "Назначение"]
                table = _create_table(doc, headers, "Методы")
                self.methods.sort(key=lambda meth: meth.name)
                for m in self.methods:
                    m.method_to_row(table)

            if len(self.properties) > 0:
                if len(self.methods) > 0:
                    doc.add_paragraph()
                headers = ['Имя', 'Модификатор доступа', "Тип", "Назначение"]
                table = _create_table(doc, headers, "Свойства")
                self.properties.sort(key=lambda pr: pr.name)
                for proper in self.properties:
                    proper.property_to_row(table)
