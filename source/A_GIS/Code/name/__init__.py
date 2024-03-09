import A_GIS.Log.function

@A_GIS.Log.function
def name(*, description: str, model="p2", tries=None):
    import ollama
    import re

    if tries == 0:
        return []

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

    content = response["message"]["content"]
    matches = re.findall(r"(A_GIS/[A-Za-z_\/]+)", content)
    result = "" if len(matches) == 0 else matches[0].replace("/", ".")

    if tries is None:
        return result
    else:
        return [result] + name(
            description=description, model=model, tries=tries - 1
        )
