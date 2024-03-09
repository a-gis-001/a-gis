def replace_block(original, block, replacement):
    import re
    # Split the block and original code into lines to handle them line by line
    original_lines = original.splitlines()
    block_lines = block.strip().splitlines()

    # Use re.escape to avoid issues with regex special characters in the block
    escaped_block_lines = [re.escape(line) for line in block_lines]

    # Build a regex pattern that matches the block with any leading whitespace
    # This pattern also captures the leading whitespace to maintain indentation
    block_pattern = r'(\s*)' + r'\s*'.join(escaped_block_lines)

    # Prepare the replacement text, preserving the original block's indentation
    # Capture group 1 (\1) is used to insert the original indentation before the replacement text
    indented_replacement = r"\1" + replacement

    # Perform the replacement
    # The flags re.MULTILINE | re.DOTALL ensure that the pattern works across multiple lines and matches newlines
    replaced_text, num_replacements = re.subn(block_pattern, indented_replacement, original, flags=re.MULTILINE | re.DOTALL, count=1)

    # Return the modified code
    return replaced_text