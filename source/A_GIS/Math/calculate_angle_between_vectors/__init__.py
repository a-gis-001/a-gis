def calculate_angle_between_vectors(*, a, b, previous_dir=[], sign=1.0):
    """Calculate the signed angle between two vectors in degrees.

    Includes an optional previous direction and an optional sign
    so that going back and forth between the same vectors has alternating
    signs, i.e. x->y->x, first calculates the angle between x,y produces +t degrees
    and y,x produces -t degrees.

    import numpy
    c=[]
    s=numpy.sign(t0)
    t1,c = A_GIS.Math.calculate_angle_between_vectors(a=x,b=y,previous_dir=c,sign=s)
    print('angle from x->y:',t1)
    s=numpy.sign(t1)
    t2,c = A_GIS.Math.calculate_angle_between_vectors(a=y,b=x,previous_dir=c,sign=s)
    print('angle from y->x:',t2)
    print('angle from x->y->x:',t1+t2)
    """
    import numpy

    # Convert to numpy arrays
    na = numpy.linalg.norm(a)
    nb = numpy.linalg.norm(b)
    a = numpy.array(a) / na
    b = numpy.array(b) / nb

    # Calculate cosine similarity
    cos_sim = numpy.dot(a, b)

    # Clip cosine similarity to avoid numerical errors
    cos_sim = numpy.clip(cos_sim, -1.0, 1.0)

    # Calculate the unsigned angle in degrees
    angle_degrees = numpy.degrees(numpy.arccos(cos_sim))

    # Determine the previous_direction of the angle (sign)
    # Compute the dot product of (a-b) to determine the sign
    c = b - a
    nc = numpy.linalg.norm(c)
    if nc > 0:
        c /= nc
        c = list(c.flatten())
    else:
        c = previous_dir

    if len(previous_dir) == len(a):
        sign *= numpy.sign(numpy.dot(previous_dir, c))

    # Apply the sign to the angle
    signed_angle = angle_degrees * sign

    return signed_angle, c
