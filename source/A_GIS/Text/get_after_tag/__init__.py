def get_after_tag(*, text: str, tag: str):
    t = text.find(tag)
    if t >= 0:
        text = text[t + len(tag) :]
    return text
