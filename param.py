import re
import string
from regex import *
from extractor import *
from setup import explicit_type_warning


class Param:

    def __init__(self, param_name: string):
        self.name = param_name
        self.type = ""
        self.comment = ""
