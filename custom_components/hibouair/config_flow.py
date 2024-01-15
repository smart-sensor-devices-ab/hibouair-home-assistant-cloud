from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol

from . import DOMAIN


class HibouairConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Hibouair integration."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # User clicked 'Submit', save the input
            return self.async_create_entry(title="Hibouair", data=user_input)

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                    vol.Required("code"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_import(self, import_config):
        """Import a configuration."""
        return await self.async_step_user(user_input=import_config)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Hibouair integration."""
    hass.data[DOMAIN] = {}
    return True
