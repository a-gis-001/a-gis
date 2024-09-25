def parse_receipt(*, image_file: str):
    """Parse an image for receipt information.

    This function takes a single parameter, `image_file`, which
    specifies the path to an image file that is suspected to contain a
    receipt. It uses AI chatbots to interpret the image and extract
    structured data about the receipt. The function returns a structured
    result containing information such as whether the image is a
    receipt, the currency and amount of the transaction, the purpose of
    the purchase, and the date of the transaction.

    The function operates in the following steps:

    1. Initializes a chatbot with a specific AI model to analyze the
       image content.
    2. Asks the chatbot to describe the contents of the image.
    3. If the chatbot identifies the image as a receipt, it proceeds
       to extract additional information using OCR (Optical Character
       Recognition) and further interactions with the chatbot.
    4. Extracts the total amount paid, the purpose of the purchase,
       and the date of the transaction by querying the chatbot with
       structured prompts.
    5. Returns a structured result containing the extracted
       information as a `dataclass` object.

    Args:
        image_file (str):
            The path to the image file that needs to be analyzed for a
            receipt.

    Returns:
        dataclass:
            A structured result object with the following attributes:

            - result (dict): A dictionary containing keys
              'is_receipt', 'currency', 'amount', 'purpose', and
              'date'.
            The values are boolean, str, float or None respectively.

            - image_desc (str): A description of the image provided to
              the chatbot.
            - image_text (str, optional): The text extracted from the
              receipt image by OCR, if applicable.
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
        result=result, image_desc=image_desc, image_text=image_text
    )
