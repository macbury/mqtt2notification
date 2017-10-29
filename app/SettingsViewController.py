from Cocoa import NSWindowController, NSApp
from Foundation import NSObject
from PyObjCTools import AppHelper
from . import (MqttCheckConfig, Alert)

import logging
import objc

logger = logging.getLogger(__name__)

class SettingsViewController(NSWindowController):
  hostTextField = objc.IBOutlet()
  portTextField = objc.IBOutlet()
  usernameTextField = objc.IBOutlet()
  passwordTextField = objc.IBOutlet()
  topicTextField = objc.IBOutlet()

  saveButton = objc.IBOutlet()
  cancelButton = objc.IBOutlet()

  loadingIndicator = objc.IBOutlet()

  app = None
  mqtt = None
  config = None

  def init(self):
    logger.info("Initializing...")
    self = objc.super(SettingsViewController, self).initWithWindowNibName_("SettingsWindow")
    return self

  @objc.python_method
  def initWithApp(self, app):
    self = objc.super(SettingsViewController, self).initWithWindowNibName_("SettingsWindow")
    self.app = app
    self.config = app.config
    self.shouldCloseDocument = True
    return self

  @objc.python_method
  def setLoading(self, loading):
    if loading:
      self.loadingIndicator.startAnimation_(self)
    else:
      self.loadingIndicator.stopAnimation_(self)
    self.saveButton.setEnabled_(not loading)
    self.hostTextField.setEnabled_(not loading)
    self.portTextField.setEnabled_(not loading)
    self.usernameTextField.setEnabled_(not loading)
    self.topicTextField.setEnabled_(not loading)
    self.passwordTextField.setEnabled_(not loading)

  def windowDidLoad(self):
    NSWindowController.windowDidLoad(self)
    self.hostTextField.setStringValue_(self.config.get_host() or '')
    self.portTextField.setIntegerValue_(self.config.get_port() or 1883)
    self.usernameTextField.setStringValue_(self.config.get_username() or '')
    self.topicTextField.setStringValue_(self.config.get_topic() or '')
    self.passwordTextField.setStringValue_(self.config.get_password() or '')
    self._.window.center()
    self.setLoading(False)
    logger.info("Window did load")

  def awakeFromNib(self):
    logger.info("Awake from nib")

  @objc.IBAction
  def onSaveSettingsClick_(self, sender):
    self.config.set_host(self.hostTextField.stringValue())
    self.config.set_topic(self.topicTextField.stringValue())
    self.config.set_username(self.usernameTextField.stringValue())
    self.config.set_port(self.portTextField.integerValue())
    self.config.set_password(self.passwordTextField.stringValue())
    self.config.save()
    self.setLoading(True)

    self.mqtt = MqttCheckConfig.create(self.config)
    self.mqtt.on_connect_success = self.on_connect_success
    self.mqtt.on_connect_error = self.on_connect_error

  @objc.IBAction
  def onCancelClick_(self, sender):
    if self.mqtt is None:
      self._.window.performClose_(self)
    else:
      self.mqtt.stop()
      self.setLoading(False)
    self.mqtt = None

  @objc.python_method
  def on_connect_success(self):
    logger.info("Connection success, config success, proceed")
    self._.window.performClose_(self)
    self.app.start_mqtt()

  @objc.python_method
  def on_connect_error(self, message):
    Alert.show_alert('Error', message)
    self.setLoading(False)
    logger.info("Connection error: " + message)

def create(app):
  view_controller = SettingsViewController.alloc().initWithApp(app)
  #NSApp.activateIgnoringOtherApps_(True)
  return view_controller