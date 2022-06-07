from typing import List, Optional
import aiohttp
from attr import define
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
import naff
from naff.client.mixins.serialization import DictSerializationMixin
from naff.client.utils.attr_utils import field
from naff.client.utils.attr_converters import optional as c_optional
from naff.client.utils.attr_converters import timestamp_converter


UTC = tz.gettz("UTC")


async def get_tourneys(region: str = "USE") -> Optional[List["Tournament"]]:
    """
    Grabs upcoming tourneys for specified region

    Regions:
        USE: US East
        USW: US West
        EU: Europe
    """
    torneys = []
    jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        async with session.get("https://rocket-league.com/tournaments") as resp:
            page_soup = BeautifulSoup(await resp.text(), "html.parser")
            raw_csrf = page_soup.find(id="window-csrf").text
            csrf_token = raw_csrf.split("=")[1].strip().strip('"')

        data = f"csrf_token={csrf_token}&region={region}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # This first request is to get the CSRF token and needed cookies

        async with session.post(
            "https://rocket-league.com/functions/updateTournamentRegionPref.php",
            data=data,
            headers=headers,
        ) as resp:
            page_soup = BeautifulSoup(await resp.text(), "html.parser")
            tourneys_html = page_soup.find_all(attrs={"class": "rlg-tournament__item"})

            for tourney_html in tourneys_html:
                tourney_soup = BeautifulSoup(str(tourney_html), "html.parser")
                if datetime_str := tourney_soup.find(
                    attrs={"class": "rlg-tournament__item-timer"}
                ):
                    time_raw = datetime.strptime(
                        datetime_str.get("data-time"), "%Y-%m-%d %H:%M:%S"
                    )
                    zone_aware_time = time_raw.replace(tzinfo=UTC)
                    time = zone_aware_time.timestamp()
                else:
                    continue

                img = tourney_soup.find(attrs={"class": "rlg-tournament__item-img"})[
                    "src"
                ]
                name = (
                    tourney_soup.find(attrs={"class": "rlg-tournament__item-info"})
                    .find("h2")
                    .text
                )
                tourney = {"timestamp": time, "img": img, "name": name}
                torneys.append(Tournament.from_dict(tourney))
    return torneys


@define()
class Tournament(DictSerializationMixin):
    name: str = field(default="N/A", repr=True)
    img: str = field(default="N/A", repr=True)
    timestamp: Optional["naff.Timestamp"] = field(
        default="In progress...", repr=True, converter=c_optional(timestamp_converter)
    )

    async def image_bytes(self) -> Optional[bytes]:
        if self.img == "N/A":
            return None
        async with aiohttp.ClientSession() as session:
            async with session.get(self.img) as resp:
                return await resp.read()
