import re
from pathlib import Path
import string

import clazz
from regex import *
from clazz import Class
from interface import Interface
from method import Method
from property import Property
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt


class Converter:

    def __init__(self, path: string):
        self.path = Path(path)
        self.classes = []
        self.interfaces = []
        self.__read_files(self.path)
        self.doc = Document()

    def __read_files(self, path: Path):
        if path.is_dir():
            for subdir in path.iterdir():
                self.__read_files(subdir)
        else:
            self.__read_file(path)

    def __read_file(self, path: Path):
        if not path.is_file():
            raise Exception("Path have to be a file")
        code = path.read_text()
        regex_for_class = get_regex_for(class_regex)
        class_matches = re.findall(regex_for_class, code, re.MULTILINE)
        for class_code in class_matches:
            c = Class(class_code[0])
            regex_for_method = get_regex_for(method_regex)
            methods = re.findall(regex_for_method, code, re.MULTILINE)
            for meth in methods:
                m = Method(meth[0])
                c.methods.append(m)

            regex_for_property = get_regex_for(property_regex)
            properties = re.findall(regex_for_property, code, re.MULTILINE)
            for pr in properties:
                p = Property(pr[0])
                c.properties.append(p)

            self.classes.append(c)

        regex_for_interface = get_regex_for(interface_regex)
        interface_matches = re.findall(regex_for_interface, code, re.MULTILINE)
        for interface_code in interface_matches:
            inter = Interface(interface_code[0])

            regex_for_method = get_regex_for(method_regex)
            methods = re.findall(regex_for_method, code, re.MULTILINE)
            for meth in methods:
                m = Method(meth[0])
                inter.methods.append(m)

            regex_for_property = get_regex_for(property_regex)
            properties = re.findall(regex_for_property, code, re.MULTILINE)
            for pr in properties:
                p = Property(pr[0])
                inter.properties.append(p)

            self.interfaces.append(inter)

    def crete_class_table(self):
        table = self.doc.add_table(1, 2)
        table.autofit = True
        table.style = 'Table Grid'
        head_cells = table.rows[0].cells
        for i, item in enumerate(['Класс', 'Назначение']):
            p = head_cells[i].paragraphs[0]
            p.add_run(item).bold = True
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
        self.classes.sort(key=lambda elm: elm.name)
        for c in self.classes:
            c.class_to_row(table)

    def crete_class_members_tables(self):
        self.classes.sort(key=lambda elm: elm.name)
        for c in self.classes:
            c.class_to_table(self.doc)

    def crete_interface_table(self):
        table = self.doc.add_table(1, 2)
        table.autofit = True
        table.style = 'Table Grid'
        head_cells = table.rows[0].cells
        for i, item in enumerate(['Интерфейс', 'Назначение']):
            p = head_cells[i].paragraphs[0]
            p.add_run(item).bold = True
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
        self.interfaces.sort(key=lambda elm: elm.name)
        for c in self.interfaces:
            c.interface_to_row(table)

    def crete_interface_members_tables(self):
        self.interfaces.sort(key=lambda elm: elm.name)
        for c in self.interfaces:
            c.interface_to_table(self.doc)

    def save_table(self, path: string):
        self.doc.save(path)
