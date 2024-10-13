def find_lines(
    *,
    image,
    xy_scale=[1, 1],
    screen_fraction=0.5,
    binary_threshold=230,
    hough_threshold=100,
    iterations=3,
    lower_canny_threshold=50,
    upper_canny_threshold=150,
    dilation_iterations=2,  # Added parameter for dilation iterations
):
    """Find lines in the image."""
    import numpy
    import cv2
    import A_GIS.Image.create_binary
    import A_GIS.Code.make_struct

    # Convert image to binary
    binary = A_GIS.Image.create_binary(image=image, threshold=binary_threshold).image
    data = numpy.array(binary)

    height, width = data.shape[:2]
    lx = int(width * screen_fraction)
    ly = int(height * screen_fraction)
    dx = 5 + xy_scale[0]  # Increased kernel size for better detection of extended lines
    dy = 5 + xy_scale[1]

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(dx), 1))
    horizontal_lines = cv2.morphologyEx(
        data, cv2.MORPH_OPEN, horizontal_kernel, iterations=iterations
    )

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(dy)))
    vertical_lines = cv2.morphologyEx(
        data, cv2.MORPH_OPEN, vertical_kernel, iterations=iterations
    )

    # Combine detected lines to create the final line mask
    lines_mask = cv2.add(horizontal_lines, vertical_lines)

    # Apply dilation to extend lines
    dilation_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    lines_mask = cv2.dilate(lines_mask, dilation_kernel, iterations=dilation_iterations)

    # Edge detection using Canny on the combined line mask
    edges = cv2.Canny(lines_mask, lower_canny_threshold, upper_canny_threshold)

    # Detecting lines using Probabilistic Hough Transform
    lines = cv2.HoughLinesP(
        edges,
        1,
        numpy.pi / 180,
        threshold=hough_threshold,
        minLineLength=min(lx, ly) // 2,  # Reduced minLineLength to detect more lines
        maxLineGap=max(dx, dy) * 2,  # Increased maxLineGap to connect fragmented lines
    )

    # Draw the detected lines on the original image for visualization
    debug_image = numpy.array(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(debug_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return A_GIS.Code.make_struct(
        binary_image=binary,
        debug_image=debug_image,
        lines=lines,
        edges=edges,
        lines_mask=lines_mask,
        _xy_scale=xy_scale,
        _screen_fraction=screen_fraction,
        _binary_threshold=binary_threshold,
        _hough_threshold=hough_threshold,
        _iterations=iterations,
        _image=image,
    )
