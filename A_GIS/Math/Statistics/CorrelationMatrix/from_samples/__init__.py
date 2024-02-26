def from_samples(*, realizations):
    """Calculate correlation coefficient from samples."""
    import numpy
    import A_GIS.Math.Statistics.CorrelationMatrix.from_numpy

    matrix = numpy.corrcoef(realizations, rowvar=False)
    return A_GIS.Math.Statistics.CorrelationMatrix.from_numpy(matrix=matrix)
