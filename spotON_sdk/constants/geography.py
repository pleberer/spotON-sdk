from dataclasses import dataclass
from entsoe import Area

@dataclass
class Country:
    name : str
    area : Area
    emoji :str
    
    def __post_init__(self):
        self.timezone = self.area.tz

@dataclass
class Markets():
    austria = Country("Austria", Area.AT,"🇦🇹")
    belgium = Country("Belgium", Area.BE,"🇧🇪")
    germany = Country("Germany", Area.DE_LU,"🇩🇪")
    france = Country("France", Area.FR,"🇫🇷")
    netherlands = Country("Netherlands", Area.NL,"🇳🇱")

    country_List = [austria,belgium,germany,france,netherlands]
