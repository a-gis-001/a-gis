"""Text utility functions.
"""
# Functions
from .add_indent import add_indent
from .apply_patch import apply_patch
from .calculate_embedding import calculate_embedding
from .diff import diff
from .extract_markdown import extract_markdown
from .find_and_replace import find_and_replace
from .get_after_tag import get_after_tag
from .get_before_tag import get_before_tag
from .get_between_tags import get_between_tags
from .get_indent import get_indent
from .get_patch import get_patch
from .get_root_word import get_root_word
from .hash import hash
from .insert_block_placeholders import insert_block_placeholders
from .reconstitute_blocks import reconstitute_blocks
from .recreate_sentence import recreate_sentence
from .reformat import reformat
from .remove_indent import remove_indent
from .replace_block import replace_block
from .slugify import slugify
from .split_first_sentence import split_first_sentence
from .split_into_sentences import split_into_sentences
from .starts_with_verb import starts_with_verb

# Packages
from . import Html
from . import Markdown
