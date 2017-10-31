"""
Mqtt platform for notify component.
"""
import logging
import json
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA, ATTR_TARGET, ATTR_TITLE, ATTR_TITLE_DEFAULT,
    PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv
import homeassistant.loader as loader

DEPENDENCIES = ['mqtt']
DOMAIN="mqtt2notification"

_LOGGER = logging.getLogger(__name__)

CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'notifications'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TOPIC): cv.string,
})

def get_service(hass, config, discovery_info=None):
  mqtt = loader.get_component('mqtt')
  topic = config.get(CONF_TOPIC, DEFAULT_TOPIC)

  return MqttNotificationService(mqtt, hass, topic)

class MqttNotificationService(BaseNotificationService):
  def __init__(self, mqtt, hass, topic):
    self.mqtt = mqtt
    self.topic = topic
    self.hass = hass

  def send_message(self, message=None, **kwargs):
    targets = kwargs.get(ATTR_TARGET)
    title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
    data = kwargs.get(ATTR_DATA)

    if not targets:
      self._push_data(title, message, data)
      _LOGGER.info("Sent notification to self")
      return
    for target in targets:
      _LOGGER.info("Pushing to multiple targets")
      self._push_data(title, message, data, target)

  def _push_data(self, title, message, data, target=None):
    payload = {
      'title': title,
      'message': message
    }
    topic = self.topic
    if target:
      topic += '/' + target
    self.mqtt.publish(self.hass, self.topic, json.dumps(payload))
