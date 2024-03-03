def new(*, low: float, mode: float, high: float):
    """
    Return a triangular distribution class.

    """
    import dataclasses
    import typing

    @dataclasses.dataclass
    class _TriDist:
        low: float
        mode: float
        high: float

        def __post_init__(self):
            if low > mode:
                raise ValueError(
                    f"Minimum value low={low} cannot be greater than mode={mode}!"
                )
            if high < mode:
                raise ValueError(
                    f"Maximum value high={high} cannot be less than mode={mode}!"
                )
            self.c = (mode - low) / (high - low)

        def sample(self, size=1):
            import scipy.stats

            return scipy.stats.triang.rvs(
                self.c, loc=self.low, scale=self.high - self.low, size=size
            )

        def pdf(self, x):
            import scipy.stats

            return scipy.stats.triang.pdf(
                x, self.c, loc=self.low, scale=self.high - self.low
            )

        def cdf(self, x):
            import scipy.stats

            return scipy.stats.triang.cdf(
                x, self.c, loc=self.low, scale=self.high - self.low
            )

        def ppf(self, q):
            import scipy.stats

            return scipy.stats.triang.ppf(
                q, self.c, loc=self.low, scale=self.high - self.low
            )

        def __repr__(self):
            return f"A_GIS.Math.Statistics.Distribution.Triangular.new(low={self.low}, mode={self.mode}, high={self.high})"

    return _TriDist(low, mode, high)
