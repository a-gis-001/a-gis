def get_before_tag(*, text: str, tag: str):
    t = text.find(tag)
    if t >= 0:
        text = text[:t]
    return text
