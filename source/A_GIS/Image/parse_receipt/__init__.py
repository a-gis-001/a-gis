def parse_receipt(*, image_file: str):
    """Parse an image to detect and extract receipt details.

    This function takes a single parameter `image_file`, which is the
    path to an image file that potentially represents a receipt. The
    function uses AI chatbots to interpret the image content and extract
    information about the receipt, such as whether it is indeed a
    receipt, the amount and currency of the transaction, the purpose of
    the purchase, and the date of the transaction.

    The function interacts with three separate AI chatbot instances,
    each specialized in different aspects of the receipt parsing
    process:

    1. The first chatbot (`A_GIS.Ai.Chatbot`) is initialized with a
       model capable of describing the contents of the image. It
       generates a description that is used by the subsequent
       chatbots to perform more specific tasks.
    2. The second and third chatbots are initialized with models that
       can understand and process natural language content related to
       receipts. They are used to extract the 'amount', 'currency',
       'purpose', and 'date' from the image description.

    The function returns an instance of a dataclass containing
    structured information about the receipt, if detected. The dataclass
    includes the following attributes:

    - `result` (dict): A dictionary with keys 'is_receipt',
      'currency', 'amount', 'purpose', and 'date'. These fields are
      populated if the image is identified as a receipt.
    - `image_file` (str): The path to the image file that was parsed.
    - `image_desc` (str): A textual description of the image provided
      by the first chatbot.
    - `image_text` (str, optional): The OCR text extracted from the
      image if it is identified as a receipt.

    Returns:
        dataclass:
            A structured object with attributes as described above.
    """
    import A_GIS.Ai.Chatbot.init
    import A_GIS.Code.make_struct
    import json

    chatbot1 = A_GIS.Ai.Chatbot.init(model="llava:34b")
    result1 = chatbot1.chat(
        message="Describe this image.", images=[image_file]
    )
    image_desc = result1.response["message"]["content"]

    result = {
        "is_receipt": False,
        "currency": None,
        "amount": None,
        "purpose": None,
        "date": None,
    }

    chatbot2 = A_GIS.Ai.Chatbot.init(model="mistral-nemo:latest")
    result2 = chatbot2.chat(
        message="Document: "
        + image_desc
        + '\n\nClaim: This describes a receipt.\n\nAnswer in JSON with key "is_receipt" and value boolean.\n\n'
    )
    j2 = json.loads(result2.response["message"]["content"])

    image_text = None
    if j2.get("is_receipt", False):

        result["is_receipt"] = True
        image_text = A_GIS.File.read_to_text(path=image_file)
        chatbot3 = A_GIS.Ai.Chatbot.init(model="mistral-nemo:latest")
        result3 = chatbot3.chat(
            message="What is the total amount paid on this receipt? Note this is an OCR result so it may be garbled.\n\n"
            + image_text.text
            + '\n\nReply in JSON with the key "amount" and the key "currency" for the 3-character type of currency, e.g. "USD" or "EUR".',
            format="json",
        )
        j3 = json.loads(result3.response["message"]["content"])
        result.update(j3)

        result4 = chatbot3.chat(
            message='What is this receipt most likely for? Reply in JSON with the key "purpose".',
            format="json",
        )
        j4 = json.loads(result4.response["message"]["content"])
        result.update(j4)

        result5 = chatbot3.chat(
            message='When was the purchase made? Reply in JSON with the key "date" in YYYY-MM-DD format.',
            format="json",
        )
        j5 = json.loads(result5.response["message"]["content"])
        result.update(j5)

    return A_GIS.Code.make_struct(
        result=result,
        image_file=image_file,
        image_desc=image_desc,
        image_text=image_text,
    )
