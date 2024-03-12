import dataclasses

@dataclasses.dataclass
class _Triangular:
    low: float
    mode: float
    high: float

    def __post_init__(self):
        if self.low > self.mode:
            raise ValueError(
                f"Minimum value low={self.low} cannot be greater than mode={self.mode}!"
            )
        if self.high < self.mode:
            raise ValueError(
                f"Maximum value high={self.high} cannot be less than mode={self.mode}!"
            )
        self.c = (self.mode - self.low) / (self.high - self.low)

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
        return f"A_GIS.Math.Distribution.Triangular.init(low={self.low}, mode={self.mode}, high={self.high})"
