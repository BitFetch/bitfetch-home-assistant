"""Details about cryptocurrencies from BitFetch."""
from datetime import timedelta
import logging
import requests

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


ATTR_PERCENT_CHANGE_24H = "percent_change_24h"
ATTR_PRICE = "price"
ATTR_PAIR = "pair"
ATTR_LAST_UPDATED = "last_updated"


ATTRIBUTION = "Data provided by BitFetch.io"

CONF_PAIR = "pair"
CONF_API_KEY = "api_key"

ICON = "mdi:currency-usd"

SCAN_INTERVAL = timedelta(minutes=5)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_PAIR): cv.string, vol.Required(CONF_API_KEY): cv.string,}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the BitFetch sensor."""
    pair = config[CONF_PAIR]
    api_key = config[CONF_API_KEY]

    try:
        BitFetchData(pair, api_key).update()
    except requests.HTTPError as error:
        if error.response.status_code == 401:
            _LOGGER.warning(
                "BitFetch API Key %s is invalid or out of API Credits", api_key
            )
        elif error.response.status_code == 403:
            _LOGGER.warning(
                "BitFetch API Key %s does not have access to this resouce. You may need to upgrade your plan at https://bitfetch.io",
                api_key,
            )
        elif error.response.status_code == 404:
            _LOGGER.warning(
                "%s is an invalid BitFetch trading pair. Trading pairs should be formatted like: BTCUSD",
                pair,
            )
        elif error.response.status_code == 500:
            _LOGGER.warning(
                "BitFetch API experienced an internal error. Please contact BitFetch support.",
            )

    add_entities(
        [BitFetchSensor(BitFetchData(pair, api_key),)], True,
    )


class BitFetchSensor(Entity):
    """Representation of a BitFetch sensor."""

    def __init__(self, data):
        """Initialize the sensor."""
        self.data = data
        self._ticker = None

    @property
    def name(self):
        """Return the name of the sensor."""
        prefix = "bitfetch_"
        return prefix + self._ticker.get("symbol")

    @property
    def state(self):
        """Return the state of the sensor."""
        return float(self._ticker.get("price"))

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        quotes = self._ticker.get("quotes")
        attrs = {}
        for q in quotes:
            attrs[q["exchange"] + "_price"] = q["price"]
            attrs[q["exchange"] + "_24h_volume"] = q["24h_volume"]

        attrs[ATTR_PERCENT_CHANGE_24H] = self._ticker.get("24h_change_pct")
        attrs[ATTR_PAIR] = self._ticker.get("symbol")
        attrs[ATTR_LAST_UPDATED] = self._ticker.get("last_updated")
        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION
        attrs["unit_of_measurement"] = self._ticker.get("symbol")
        return attrs

    def update(self):
        """Get the latest data and updates the states."""
        self.data.update()
        self._ticker = self.data.ticker.get("data")


class BitFetchData:
    """Get the latest data and update the states."""

    def __init__(self, pair, api_key):
        """Initialize the data object."""
        self.pair = pair
        self.api_key = api_key
        self.ticker = None

    def update(self):
        """Get the latest data from bitfetch.io."""
        url = "https://api.bitfetch.io/v1/price/pairs/"
        headers = {"Authorization": self.api_key}
        data = requests.request("GET", url + self.pair, timeout=2, headers=headers)
        data.raise_for_status()
        self.ticker = data.json()
