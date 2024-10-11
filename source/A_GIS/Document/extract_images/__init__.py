def extract_images(
    *,
    pdf_path,
    filename="page{page_number}_image{image_number}",
    output_dir=None,
):
    """Extract images from a PDF."""

    import fitz  # PyMuPDF
    import os
    import dataclasses
    import A_GIS.Code.make_struct

    # Ensure output directory exists
    if output_dir is not None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    @dataclasses.dataclass
    class Pdf_Image:
        page_number: int
        image_number: int
        ext: str
        image_bytes: list

    # Iterate through all pages and images
    image_list = []
    image_paths = []
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        images = page.get_images(full=True)

        image_number = 0
        for img_index, img in enumerate(images):
            image_number += 1
            xref = img[0]  # The xref of the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = (
                filename.format(
                    page_number=page_number, image_number=image_number
                )
                + "."
                + image_ext
            )

            # Write the image file
            if output_dir is not None:
                image_path = os.path.join(output_dir, image_filename)
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                image_paths.append(image_path)
            else:
                image_list.append(
                    Pdf_Image(
                        page_number=page_number,
                        image_bytes=image_bytes,
                        image_number=img_index,
                        ext=ext,
                    )
                )

    pdf_document.close()
    return A_GIS.Code.make_struct(
        _pdf_path=pdf_path,
        _filename=filename,
        _output_dir=output_dir,
        image_paths=image_paths,
        image_list=image_list,
    )
