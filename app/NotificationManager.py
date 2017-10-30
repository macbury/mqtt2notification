from Foundation import (NSDictionary, NSObject)
from AppKit import (NSUserNotification, NSUserNotificationCenter)
import objc

class NotificationManager(NSObject):
  def init(self):
    self = objc.super(NotificationManager, self).init()
    self.notification_center = NSUserNotificationCenter.defaultUserNotificationCenter()
    self.notification_center.setDelegate_(self)
    myDict = NSDictionary.dictionary()
    return self

  @objc.python_method
  def show(self, title, text):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    #notification.setIdentifier_("ID_1")
    notification.setInformativeText_(str(text))
    notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setHasActionButton_(True)
    notification.setActionButtonTitle_("View")

    payload = NSDictionary.dictionary()

    notification.setUserInfo_(payload)
    self.notification_center.scheduleNotification_(notification)
    return notification

  @objc.python_method
  def clear(self):
    self.notification_center.removeAllDeliveredNotifications()

  def userNotificationCenter_didActivateNotification_(self, center, notification):
    userInfo = notification.userInfo()
    print(userInfo)

def create():
  return NotificationManager.alloc().init()