from PyObjCTools import AppHelper
from Foundation import (NSObject, NSAlert)

def show_alert(title, body):
  AppHelper.callAfter(showAlert_, title, body)

def showAlert_(title, body):
  alertWindow = NSAlert.alloc().init()
  alertWindow.addButtonWithTitle_("Understood")
  alertWindow.setMessageText_(title)
  alertWindow.setInformativeText_(body)
  alertWindow.runModal()