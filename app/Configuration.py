from Foundation import (NSObject, NSUserDefaults)

import keyring
import keyring.backends.kwallet
import keyring.backends.OS_X
import keyring.backends.SecretService
import keyring.backends.Windows

CONF_SERVICE = "mqtt2notification"
CONF_HOST = 'host'
CONF_PORT = 'port'
CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'
CONF_TOPIC = 'topic'

class Configuration:
  def __init__(self):
    self.data = NSUserDefaults.standardUserDefaults()
  def get_password(self):
    return keyring.get_password(CONF_SERVICE, CONF_PASSWORD)
  def get_username(self):
    return self.data.stringForKey_(CONF_USERNAME)
  def get_topic(self):
    return self.data.stringForKey_(CONF_TOPIC)
  def get_host(self):
    return self.data.stringForKey_(CONF_HOST)
  def get_port(self):
    return self.data.integerForKey_(CONF_PORT)
  def set_host(self, host):
    self.data.setObject_forKey_(host, CONF_HOST)
  def set_port(self, port):
    self.data.setObject_forKey_(port, CONF_PORT)
  def set_topic(self, topic):
    self.data.setObject_forKey_(topic, CONF_TOPIC)
  def set_username(self, username):
    self.data.setObject_forKey_(username, CONF_USERNAME)
  def set_password(self, password):
    keyring.set_password(CONF_SERVICE, CONF_PASSWORD, password)
  def exists(self):
    return self.get_host() is not None

  def save(self):
    self.data.synchronize()

def create():
  return Configuration()