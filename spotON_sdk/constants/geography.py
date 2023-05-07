from dataclasses import dataclass
from entsoe import Area
import pandas as pd

from dataclasses import dataclass, field
from typing import Optional, Dict
import pytz

from typing import List

def _default_capitals() -> Dict[str, str]:
    return {
        "Austria": "Europe/Vienna",
        "Belgium": "Europe/Brussels",
        "Bulgaria": "Europe/Sofia",
        "Croatia": "Europe/Zagreb",
        "Cyprus": "Asia/Nicosia",
        "Czech Republic": "Europe/Prague",
        "Denmark": "Europe/Copenhagen",
        "Estonia": "Europe/Tallinn",
        "Finland": "Europe/Helsinki",
        "France": "Europe/Paris",
        "Germany": "Europe/Berlin",
        "Greece": "Europe/Athens",
        "Hungary": "Europe/Budapest",
        "Ireland": "Europe/Dublin",
        "Italy": "Europe/Rome",
        "Latvia": "Europe/Riga",
        "Lithuania": "Europe/Vilnius",
        "Luxembourg": "Europe/Luxembourg",
        "Malta": "Europe/Malta",
        "Netherlands": "Europe/Amsterdam",
        "Poland": "Europe/Warsaw",
        "Portugal": "Europe/Lisbon",
        "Romania": "Europe/Bucharest",
        "Slovakia": "Europe/Bratislava",
        "Slovenia": "Europe/Ljubljana",
        "Spain": "Europe/Madrid",
        "Sweden": "Europe/Stockholm",
    }

def _country_code_to_emoji(country_code):
    OFFSET = 127397
    return ''.join(chr(ord(c) + OFFSET) for c in country_code.upper())

@dataclass
class EuropeanCapitals:
    capitals: Dict[str, str] = field(default_factory=_default_capitals)

    def get_timedelta(self, tz_str: str) -> Optional[pd.Timedelta]:
        tz_capitals = {v: k for k, v in self.capitals.items()}
        if tz_str in tz_capitals:
            local_tz = pytz.timezone(tz_str)
            utc_dt = pd.Timestamp.utcnow().to_pydatetime()
            local_dt = utc_dt.astimezone(local_tz)
            UTC_time_difference = (local_dt.utcoffset().total_seconds()) // 3600
            delta = pd.Timedelta(hours=UTC_time_difference)
            capital = tz_str.split("/")[1]
            return delta,UTC_time_difference,capital
        else:
            print(f"{tz_str} not found in European capitals.")
            return None




@dataclass
class Country:
    full_name : str
    area : list[Area]

    
    def __post_init__(self):
        self.emoji = _country_code_to_emoji(self.area[0].name)
        delta,UTC_time_difference,capital = EuropeanCapitals().get_timedelta(self.area[0].tz)
        self.capital = capital
        self.timezone_UTC_time_difference = UTC_time_difference
        self.timezone_delta = delta
        self.timezone_string = f"UTC +{self.timezone_UTC_time_difference}"
        self.name = f"{self.full_name} {self.emoji}"

@dataclass
class Markets():
    austria = Country("Austria", [Area.AT])
    belgium = Country("Belgium", [Area.BE])
    germany = Country("Germany", [Area.DE_LU])
    france = Country("France", [Area.FR])
    netherlands = Country("Netherlands", [Area.NL])
    sweden = Country("Sweden", [Area.SE_1,Area.SE_2,Area.SE_3,Area.SE_4])

    # Add all Countries
    country_List = [value for key, value in vars().items() if isinstance(value, Country)]

    @staticmethod
    def get_Market_by_area_code(area_code: str) -> Optional[Country]:
        for country in Markets.country_List:
            for area in country.area:
                if area.name == area_code:
                    return country

        return None




