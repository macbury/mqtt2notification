from Foundation import (NSObject)
from . import (NotificationManager, SettingsViewController, Configuration, MqttNotificationRelay, Alert)
from AppKit import NSMenu, NSMenuItem, NSApplication, NSStatusBar, NSImage, NSVariableStatusItemLength
import logging
import objc

logger = logging.getLogger(__name__)

class MyAppDelegate(NSObject):
  settingsViewController = None
  notifications = None
  config = None
  mqtt = None
  menu = None
  nsstatusitem = None

  def init(self):
    logger.info("Initializing...")
    self.config = Configuration.create()
    self.create_ui()
    self.notifications = NotificationManager.create()
    self.notifications.clear()
    self.settingsViewController = SettingsViewController.create(self)
    if self.config.exists():
      self.start_mqtt()
    else:
      self.show_settings()
    return self

  @objc.python_method
  def start_mqtt(self):
    if self.mqtt is not None:
      self.mqtt.stop()
    logger.info("Start mqtt...")
    self.mqtt = MqttNotificationRelay.create(self.config, self.notifications)

  @objc.python_method
  def show_settings(self):
    self.settingsViewController.showWindow_(self)
    NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    logger.info("Showing settings...")

  def applicationDidFinishLaunching_(self, notification):
    logger.info("Application did finish launching...")

  @objc.python_method
  def create_ui(self):
    icon = NSImage.alloc().initByReferencingFile_('main.icns')
    icon.setScalesWhenResized_(True)
    icon.setSize_((20, 20))
    self.menu = NSMenu.alloc().init()

    configureMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Configure', 'clickedConfigure:', '')
    self.menu.addItem_(configureMenuItem)

    quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
    self.menu.addItem_(quit)

    self.nsstatusitem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
    self.nsstatusitem.setImage_(icon)
    self.nsstatusitem.setHighlightMode_(True)
    self.nsstatusitem.setMenu_(self.menu)

  def clickedConfigure_(self, notification):
    logger.info("Clicked configure")
    self.show_settings()

def create():
  return MyAppDelegate.alloc().init()