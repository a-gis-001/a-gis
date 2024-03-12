def from_samples(*, realizations):
    """Calculate correlation coefficient from samples."""
    import numpy
    import A_GIS.Math.CorrelationMatrix.init_from_numpy

    matrix = numpy.corrcoef(realizations, rowvar=False)
    return A_GIS.Math.CorrelationMatrix.init_from_numpy(matrix=matrix)
