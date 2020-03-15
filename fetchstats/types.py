import attr

@attr.s
class RegionReport():
    state = attr.ib()
    country = attr.ib()
    last_update = attr.ib()
    confirmed_cases = attr.ib(factory=int, converter=int)
    deaths = attr.ib(factory=int, converter=int)
    recovered_cases = attr.ib(factory=int, converter=int)
    lat = attr.ib(factory=float, converter=float)
    long = attr.ib(factory=float, converter=float)


