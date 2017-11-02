import paho.mqtt.client as mqtt
import ssl
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MqttController:
  def __init__(self, config):
    
    logger.info("Initializing connection")
    self.config = config
    self.client = mqtt.Client()
    self.client.on_connect = self.on_connect
    self.client.on_message = self.on_message
    self.client.on_disconnect = self.on_disconnect
    self.client.enable_logger(logger)
    self.client.tls_set_context(ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))

    if self.config.get_username() is not None:
      logger.info("Configuring authentication login")
      self.client.username_pw_set(self.config.get_username(), self.config.get_password())

    logger.info("Connecting to: " + self.config.get_host() + ":" +str(self.config.get_port()))
    self.client.connect_async(self.config.get_host(), self.config.get_port(), 10)
    logger.info("Starting loop")
    self.client.loop_start()

  def stop(self):
    self.client.disconnect()

  def on_connect(self, client, userdata, flags, rc):
    logger.info("On connect")

  def on_message(self, client, userdata, msg):
    logger.info("On message")

  def on_disconnect(self, client, userdata, rc):
    logger.info("On Disconnect")