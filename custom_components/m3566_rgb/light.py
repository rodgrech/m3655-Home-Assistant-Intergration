"""Light platform for M3566 RGB Controller."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    ATTR_RGB_COLOR,
    ATTR_XY_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import color as color_util

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
    _attr_icon = "mdi:led-strip-variant"
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB

    def __init__(self, entry: ConfigEntry, client: M3566ApiClient, coordinator) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_rgb_light"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry.data[CONF_HOST]}:{client.port}")},
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
        if kwargs.get(ATTR_BRIGHTNESS) == 0:
            state = await self._client.async_turn_off()
        else:
            red, green, blue = self._rgb_from_kwargs(kwargs)
            state = await self._client.async_set_rgb(red, green, blue)

        self.coordinator.async_set_updated_data(state)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        state = await self._client.async_turn_off()
        self.coordinator.async_set_updated_data(state)

    def _rgb_from_kwargs(self, kwargs: dict[str, Any]) -> tuple[bool, bool, bool]:
        """Convert Home Assistant color input to the tablet's binary RGB channels."""
        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
        elif ATTR_HS_COLOR in kwargs:
            hue, saturation = kwargs[ATTR_HS_COLOR]
            rgb = color_util.color_hs_to_RGB(hue, saturation)
        elif ATTR_XY_COLOR in kwargs:
            x_value, y_value = kwargs[ATTR_XY_COLOR]
            rgb = color_util.color_xy_to_RGB(x_value, y_value)
        else:
            return (True, True, True)

        return self._quantize_rgb(rgb)

    @staticmethod
    def _quantize_rgb(rgb: tuple[float, float, float]) -> tuple[bool, bool, bool]:
        """Map smooth RGB values to this hardware's eight binary color states."""
        red, green, blue = (max(0, min(255, int(value))) for value in rgb)
        strongest = max(red, green, blue)
        if strongest <= 0:
            return (False, False, False)

        threshold = max(32, int(strongest * 0.4))
        return (red >= threshold, green >= threshold, blue >= threshold)
