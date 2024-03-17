def generate(*, description: str = "", **kwargs):
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Code.distill
    import A_GIS.Code.format
    import A_GIS.Code.extract_python

    coder = A_GIS.Ai.Chatbot.init(
        system="""
A_GIS is repository for aritificial-intelligence driven functional code.

An A_GIS functional unit is just a function, by itself in a file, with the following guidelines.

1. All imports should be absolute and inside the function.
2. All arguments are keyword arguments with type hints. Any types needed for type hints
   beyond `import typing` the standard ones should use the runtime type checking
   of the form `type['MyType']`.
3. The function is pure, meaning it does not modify their arguments or have global parameters.
4. Each function should be short, 10 lines or less. The function body can define nested functions
   which do not count towards the 10 line limit.
5. Imports must be absolute without renames, e.g. `import matplotlib.pyplot` and NOT
   `import matplotlib.pyplot as plt` or `import matplotlib.pyplot
`.

You are the primary code developer for a new A_GIS functional unit and will
create a short concise functional unit, given a request from your manager.
Your code will be short and concise WITHOUT COMMENTS and WITHOUT EXAMPLES and contained
in a Markdown block e.g.,

```python
<your A_GIS functional unit code here>
```
""",
        **kwargs,
    )

    result = coder.chat(message=description)
    content = result["message"]["content"]

    return A_GIS.Code.extract_python(text=content)
