from . import MqttController
import paho.mqtt.client as mqtt

class MqttCheckConfig(MqttController.MqttController):
  on_connect_success = None
  on_connect_error = None

  def __init__(self, config):
    MqttController.MqttController.__init__(self, config)
    self.client.reconnect_delay_set(1, 2)

  def on_connect(self, client, userdata, flags, rc):
    self.stop()
    if rc == mqtt.CONNACK_ACCEPTED: # success
      print("Success works")
      self.on_connect_success()
    else:
      if self.on_connect_error is not None:
        self.on_connect_error(mqtt.connack_string(rc))


def create(config):
  return MqttCheckConfig(config)