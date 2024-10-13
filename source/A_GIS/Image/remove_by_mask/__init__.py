def remove_by_mask(*, image, mask, bg_color=255):
    import A_GIS.Code.make_struct
    import PIL
    import numpy

    # Load the original image (assuming it's an RGB NumPy array)
    image_array = numpy.array(image)

    # Ensure that the mask is a binary mask (0 or 255)
    mask_array = numpy.array(mask, dtype=numpy.uint8)

    # Convert the mask to a Boolean mask where True represents regions to
    # discard
    boolean_mask = mask_array == 255

    # Create a copy of the original image to modify
    masked_image = image_array

    # If the image is RGB, repeat the mask for each of the 3 channels
    if len(image_array.shape) == 3 and image_array.shape[2] == 3:
        boolean_mask_rgb = numpy.repeat(
            boolean_mask[:, :, numpy.newaxis], 3, axis=2
        )

        # Apply the Boolean mask: keep original values where mask is True
        masked_image[boolean_mask_rgb] = 255
    else:
        # If the image is grayscale (single channel), use the Boolean mask
        # directly
        masked_image[boolean_mask] = 255

    return A_GIS.Code.make_struct(image=PIL.Image.fromarray(masked_image))
