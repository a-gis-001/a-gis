def name(*, description: str, model="p2"):
    import ollama
    import re

    response = ollama.chat(
        model="p2",
        messages=[
            {
                "role": "user",
                "content": "the A_GIS function (new or existing) to"
                + description,
            }
        ],
    )
    content = response["content"]
    matches = re.findall(r"(A_GIS/[A-Za-z_\/]+)", content)
    if len(matches) == 0:
        return ""
    else:
        return matches[0]
