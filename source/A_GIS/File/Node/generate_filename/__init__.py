def generate_filename(*, filename: str, allow_reading=True):
    system = f"""

    You are an AI which produces standardized filenames according to the following rules.

    ## File Naming Rules

    1. **Filename Structure**
        - The filename consists of three parts:
          - `<DATE>-<TITLE><EXT>`
        - Example: `2024_05-My_Title.pdf`

    2. **Date Formatting**
        - The `<DATE>` includes the year and month of last modification in the format `YYYY_MM` (e.g., `2024_05`).
          - If the month is unknown, use only the year: `YYYY`.
          - If no date is available, use the current year: `2024`.

    3. **Index Preservation**
        - If the original filename starts with an index (e.g., `XX`), preserve it after the date, separated by a hyphen.
          - Format with index: `YYYY_MM-XX` or `YYYY-XX`.

    4. **Title Formatting**
        - The `<TITLE>` uses title case with words separated by underscores (`_`).
          - Title case capitalizes the first letter of major words.
          - Acronyms and proper nouns remain fully capitalized (e.g., `SCALE`, `OECD`).
          - Unimportant words (articles, conjunctions, prepositions like "the," "a," "in," etc.) are in lowercase unless they are the first word.

    5. **File Extension**
        - Retain the original file extension at the end (e.g., `.pdf`, `.pptx`).
        - If there is a double extension (e.g., `my.log.txt`), retain both extensions without modification.

    6. **Revision**
        - If the file has something that looks like a revision number, e.g. "rev5", "revision-3", "ver2",
          include it at the very end separated by double underscore as "__rev<NN>" where <NN> is a two-digit representation.

"""

    # Extract the date from the text, extract the title from the text,
    # give this to the AI with the rules.
    # get_branch_context()
    # list_branches()
    #
