def generate(*, name: str, code: str, **kwargs):
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Code.distill
    import A_GIS.Code.reformat
    import A_GIS.Code.extract_python
    import A_GIS.Text.get_after_tag
    import A_GIS.Text.get_before_tag

    coder = A_GIS.Ai.Chatbot.init(
        system="""
You are a world-class test creator for Python programs in the
A_GIS code system. A_GIS is a collection of Python adhering to
functional programming tenets with special considerations for
reproducibility by supporting transformations of source using
`import A_GIS.*` to special hashed function names that ensure
backwards compatibility forever. For this reason, A_GIS ALWAYS
uses absolute imports, even in tests. For all modules.

Here is an example.

### Instruction:

name:
    A_GIS.File.hash

code:

    def hash(*, file: type["pathlib.Path"]):
        import hashlib

        sha256_hash = hashlib.sha256()
        with open(file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

### Response:

tests:

    import pytest
    import A_GIS.File.hash
    import pathlib

    def test_determinism(tmp_path: pathlib.Path):
        test_content = b"Hello, World!"
        test_file = tmp_path / "test_file.txt"
        test_file.write_bytes(test_content)

        # Compute the hash twice for the same content
        first_hash = A_GIS.File.hash(file=test_file)
        second_hash = A_GIS.File.hash(file=test_file)

        # Verify that both hashes are the same
        assert (
            first_hash == second_hash
        ), "The hash function should produce the same output for the same input"

    def bit_difference(hash1: str, hash2: str) -> int:
        # Convert hex hashes to binary representation, stripping the '0b' prefix
        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)

        # Count the differing bits
        return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))

    def test_avalanche_effect(tmp_path: pathlib.Path):
        # Create two temporary files with content that differs by a small amount
        original_content = b"Hello, World!"
        modified_content = b"hello, World!"  # Small change: 'H' -> 'h'

        original_file = tmp_path / "original.txt"
        modified_file = tmp_path / "modified.txt"

        original_file.write_bytes(original_content)
        modified_file.write_bytes(modified_content)

        # Compute hashes
        original_hash = A_GIS.File.hash(file=original_file)
        modified_hash = A_GIS.File.hash(file=modified_file)

        # Calculate bit difference
        difference = bit_difference(original_hash, modified_hash)

        # Assuming SHA-256 hash function, which produces 256-bit hash
        # We expect a significant difference, for simplicity, let's say at least 25% of the bits should differ
        expected_min_difference = 256 * 0.25  # 25% of 256 bits

        assert (
            difference >= expected_min_difference
        ), "A small change in input should significantly change the output hash."

    def test_collision_resistance(tmp_path: pathlib.Path):
        first_content = b"Hello, World!"
        second_content = b"Goodbye, World!"

        first_file = tmp_path / "first_file.txt"
        second_file = tmp_path / "second_file.txt"

        first_file.write_bytes(first_content)
        second_file.write_bytes(second_content)

        # Compute the hashes
        first_hash = A_GIS.File.hash(file=first_file)
        second_hash = A_GIS.File.hash(file=second_file)

        # Verify that the hashes are different
        assert (
            first_hash != second_hash
        ), "Different inputs should not produce the same hash"

""",
        **kwargs,
    )

    indented_code = A_GIS.Text.add_indent(text=code)
    message = f"name:\n    {name}code:\n{indented_code}\n"

    result = coder.chat(message=message)
    content = result["message"]["content"]

    content = A_GIS.Text.get_after_tag(text=content, tag="tests:")
    content = A_GIS.Text.get_before_tag(text=content, tag="### Instruction:")

    return A_GIS.Code.extract_python(text=content)
