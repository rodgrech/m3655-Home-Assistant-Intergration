"""Light platform for M3566 RGB Controller."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import ATTR_RGB_COLOR, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import M3566ApiClient
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up M3566 RGB light entity."""
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            M3566RgbLight(
                entry=entry,
                client=data["client"],
                coordinator=data["coordinator"],
            )
        ]
    )


class M3566RgbLight(CoordinatorEntity, LightEntity):
    """Representation of the tablet RGB light strip."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB

    def __init__(self, entry: ConfigEntry, client: M3566ApiClient, coordinator) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_rgb_light"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data[CONF_NAME],
            manufacturer="M3566 / RK3566",
            model="Android RGB wall tablet",
            configuration_url=f"http://{entry.data[CONF_HOST]}:{client.port}",
        )

    @property
    def is_on(self) -> bool:
        """Return true if any RGB channel is on."""
        return bool(self.coordinator.data.get("on", False))

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return RGB color from the channel state."""
        data = self.coordinator.data
        return (
            255 if data.get("red") else 0,
            255 if data.get("green") else 0,
            255 if data.get("blue") else 0,
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        if ATTR_RGB_COLOR in kwargs:
            red, green, blue = kwargs[ATTR_RGB_COLOR]
            state = await self._client.async_set_rgb(red > 0, green > 0, blue > 0)
        else:
            state = await self._client.async_set_rgb(True, True, True)

        self.coordinator.async_set_updated_data(state)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        state = await self._client.async_turn_off()
        self.coordinator.async_set_updated_data(state)
