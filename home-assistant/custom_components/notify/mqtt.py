"""
Mqtt platform for notify component.
"""
import logging

import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA, ATTR_TARGET, ATTR_TITLE, ATTR_TITLE_DEFAULT,
    PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv
import homeassistant.loader as loader

DEPENDENCIES = ['mqtt']

_LOGGER = logging.getLogger(__name__)

CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'notifications'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TOPIC): cv.string,
})

def get_service(hass, config, discovery_info=None):
  mqtt = loader.get_component('mqtt')
  topic = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC)

  return MqttNotificationService(mqtt, topic)

class MqttNotificationService(BaseNotificationService):
  def __init__(self, mqtt, topic):
    self.mqtt = mqtt
    self.topic = topic

    def send_message(self, message=None, **kwargs):
