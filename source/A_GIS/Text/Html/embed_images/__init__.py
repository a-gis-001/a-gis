def embed_images(*, html, base_path="."):
    """Replace local image sources with Base64-encoded versions using BeautifulSoup."""
    import os
    import base64
    from bs4 import BeautifulSoup

    def encode_image_to_base64(img_path):
        """Convert an image file to a base64 data URI."""
        try:
            with open(img_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"Warning: Image not found: {img_path}")
            return None

    soup = BeautifulSoup(html, "html.parser")

    for img_tag in soup.find_all("img"):
        img_src = img_tag.get("src")

        # Handle absolute and relative paths
        img_path = img_src if os.path.isabs(img_src) else os.path.join(base_path, img_src.lstrip("/"))

        if os.path.exists(img_path):
            ext = os.path.splitext(img_path)[1][1:]  # Extract file extension
            mime_type = f"image/{ext}" if ext in ["png", "jpg", "jpeg", "gif"] else "image/png"
            base64_img = encode_image_to_base64(img_path)
            if base64_img:
                img_tag["src"] = f"data:{mime_type};base64,{base64_img}"
        else:
            print(f"Image not found: {img_path}")

    return str(soup)
