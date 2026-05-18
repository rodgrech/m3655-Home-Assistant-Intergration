"""Client for the M3566 RGB Controller Android app."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientSession


class M3566ApiError(Exception):
    """Raised when the M3566 controller API cannot be reached or returns bad data."""


@dataclass(slots=True)
class M3566ApiClient:
    """Tiny HTTP client for the tablet-side RGB bridge."""

    session: ClientSession
    host: str
    port: int = 8765

    @property
    def base_url(self) -> str:
        """Return the controller base URL."""
        return f"http://{self.host}:{self.port}"

    async def async_status(self) -> dict[str, bool]:
        """Fetch the current light state."""
        data = await self._request_json("/status")
        return {
            "red": bool(data.get("red")),
            "green": bool(data.get("green")),
            "blue": bool(data.get("blue")),
            "on": bool(data.get("on")),
        }

    async def async_set_rgb(self, red: bool, green: bool, blue: bool) -> dict[str, bool]:
        """Set the RGB channels."""
        data = await self._request_json(
            f"/set?red={int(red)}&green={int(green)}&blue={int(blue)}"
        )
        if not data.get("ok", False):
            raise M3566ApiError(str(data.get("result", "controller rejected command")))
        state = data.get("state")
        if not isinstance(state, dict):
            return await self.async_status()
        return {
            "red": bool(state.get("red")),
            "green": bool(state.get("green")),
            "blue": bool(state.get("blue")),
            "on": bool(state.get("on")),
        }

    async def async_turn_off(self) -> dict[str, bool]:
        """Turn off all channels."""
        data = await self._request_json("/color/off")
        if not data.get("ok", False):
            raise M3566ApiError(str(data.get("result", "controller rejected command")))
        state = data.get("state")
        if not isinstance(state, dict):
            return await self.async_status()
        return {
            "red": bool(state.get("red")),
            "green": bool(state.get("green")),
            "blue": bool(state.get("blue")),
            "on": bool(state.get("on")),
        }

    async def _request_json(self, path: str) -> dict[str, Any]:
        """Make a GET request and parse JSON."""
        try:
            async with asyncio.timeout(5):
                response = await self.session.get(f"{self.base_url}{path}")
                response.raise_for_status()
                data = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as err:
            raise M3566ApiError(f"Failed to call {self.base_url}{path}: {err}") from err

        if not isinstance(data, dict):
            raise M3566ApiError("Controller returned an unexpected response")
        return data
