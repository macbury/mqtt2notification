from . import MqttController
import paho.mqtt.client as mqtt
import json
import logging
logger = logging.getLogger(__name__)

class Notification:
  title = None
  message = None
  def __init__(self, raw_json):
    self.raw_json = raw_json
    try:
      logger.info('[Got json]: {}'.format(raw_json))
      raw_notification = json.loads(raw_json)
      self.title = raw_notification['title']
      self.message = raw_notification['message']
    except Exception as e:
      logger.error(e)
  def is_valid(self):
    return self.title is not None or self.message is not None

class MqttNotificationRelay(MqttController.MqttController):

  def __init__(self, config, notifications):
    MqttController.MqttController.__init__(self, config)
    self.notifications = notifications

  def on_connect(self, client, userdata, flags, rc):
    logger.info("Connected, subscribing to: " + self.config.get_topic())
    self.client.subscribe(self.config.get_topic()) 

  def on_message(self, client, userdata, msg):
    notification = Notification(msg.payload)
    if notification.is_valid():
      self.notifications.show(notification.title, notification.message)
    else:
      logger.error("Notification is invalid")

def create(config, notifications):
  return MqttNotificationRelay(config, notifications)