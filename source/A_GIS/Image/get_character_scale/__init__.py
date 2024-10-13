def get_character_scale(
    *,
    image,
    threshold=150,
    min_area=10,
    iterations=2,
    min_area_multiplier=0.1,
    tolerance=0.01,
):
    """Get character scale."""
    import numpy
    import cv2
    import matplotlib.pyplot
    import A_GIS.Image.create_binary
    import A_GIS.Code.make_struct
    import math

    result = A_GIS.Image.create_binary(image=image, threshold=threshold)
    binary = numpy.array(result.image)

    # Find contours
    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    debug_images = []
    min_areas = []
    xy_scales = []
    widths = []
    heights = []
    min_areas.append(min_area)
    for i in range(iterations):

        # Filter contours based on size to remove noise
        character_contours = [
            c for c in contours if cv2.contourArea(c) > min_area
        ]

        for contour in character_contours:
            _, _, w, h = cv2.boundingRect(contour)
        widths.append(w)
        heights.append(h)

        # Visualize detected characters
        d = numpy.array(image)
        for contour in character_contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(d, (x, y), (x + w, y + h), (0, 255, 0), 1)
        d = cv2.cvtColor(d, cv2.COLOR_BGR2RGB)

        if len(widths) > 0:
            avg_width = numpy.median(widths)  # Use median instead of mean
            avg_height = numpy.median(heights)
            min_area = min_area_multiplier * avg_width * avg_height
        else:
            min_area *= min_area_multiplier

        debug_images.append(d)
        xy_scales.append([avg_width, avg_height])
        min_areas.append(min_area)
        if math.fabs(min_areas[-1] / min_areas[-2] - 1) < tolerance:
            break

    return A_GIS.Code.make_struct(
        xy_scale=xy_scales[-1],
        xy_scales=xy_scales,
        binary_image=binary,
        debug_images=debug_images,
        min_areas=min_areas,
        _min_area=min_area,
        _iterations=iterations,
        _threshold=threshold,
        _image=image,
        _min_area_multiplier=min_area_multiplier,
    )
