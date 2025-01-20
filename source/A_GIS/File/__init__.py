"""Collection of file operations.
"""
# Functions
from ._read_to_text_docx import _read_to_text_docx
from ._read_to_text_pdf import _read_to_text_pdf
from ._read_to_text_pptx import _read_to_text_pptx
from .delete import delete
from .download import download
from .find_and_replace import find_and_replace
from .glob import glob
from .guess_year import guess_year
from .hash import hash
from .is_subdirectory import is_subdirectory
from .is_url import is_url
from .make_directory import make_directory
from .open import open
from .read import read
from .read_to_text import read_to_text
from .should_ignore import should_ignore
from .show_tree import show_tree
from .touch import touch
from .write import write

# Classes
from ._Modification_Handler import _Modification_Handler
from ._Url import _Url

# Packages
from . import Duplicates
from . import Management
from . import Node
