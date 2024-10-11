def find_lines(*,
    image,
    xy_scale=[1,1],
    screen_fraction=0.5,
    binary_threshold=150,
    hough_threshold=100,
    iterations=2,
    lower_canny_threshold=50,
    upper_canny_threshold=150,
):
    """Find lines in the image."""
    import numpy
    import cv2
    import matplotlib.pyplot
    import A_GIS.Image.create_binary
    import A_GIS.Code.make_struct
    import math

    binary = A_GIS.Image.create_binary(image=image, threshold=binary_threshold).image
    data = numpy.array(binary)

    height, width = data.shape[:2]
    lx = int(width*screen_fraction)
    ly = int(height*screen_fraction)
    dx = xy_scale[0]
    dy = xy_scale[1]

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (dx, 1))
    horizontal_lines = cv2.morphologyEx(data, cv2.MORPH_OPEN, horizontal_kernel, iterations=iterations)

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, dy))
    vertical_lines = cv2.morphologyEx(data, cv2.MORPH_OPEN, vertical_kernel, iterations=iterations)

    # Combine detected lines to create the final line mask
    lines_mask = cv2.add(horizontal_lines, vertical_lines)

    # Edge detection using Canny on the combined line mask
    edges = cv2.Canny(lines_mask, lower_canny_threshold, upper_canny_threshold)

    # Detecting lines using Probabilistic Hough Transform
    lines = cv2.HoughLinesP(edges, 1, numpy.pi / 180, threshold=hough_threshold, minLineLength=min(lx,ly), maxLineGap=min(dx,dy))

    # Draw the detected lines on the original image for visualization
    debug_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_GRAY2BGR)  # Convert grayscale to color for drawing lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(debug_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return A_GIS.Code.make_struct(
        binary_image=binary,
        debug_image=debug_image,
        _xy_scale=xy_scale,
        _screen_fraction=screen_fraction,
        _binary_threshold=binary_threshold,
        _hough_threshold=hough_threshold,
        _iterations=iterations,
        _image=image,
    )
