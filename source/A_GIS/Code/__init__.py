"""Generic functions whose key input/output is a code string.
"""
# Functions
from ._distill_imports import _distill_imports
from .convert_multiline import convert_multiline
from .distill import distill
from .extract_python import extract_python
from .find_root import find_root
from .generate import generate
from .get_schema import get_schema
from .get_source import get_source
from .guess_name import guess_name
from .guess_type import guess_type
from .highlight import highlight
from .is_class import is_class
from .is_function import is_function
from .is_package import is_package
from .is_program import is_program
from .list import list
from .make_struct import make_struct
from .parse_docstring import parse_docstring
from .reformat import reformat
from .replace_docstring import replace_docstring
from .replace_from_imports import replace_from_imports

# Packages
from . import CommitMessage
from . import Docstring
from . import Tree
from . import Unit
