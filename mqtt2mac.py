from Foundation import NSApplication
from PyObjCTools import AppHelper
from AppKit import NSApp

from app import (MyAppDelegate)

import objc
objc.setVerbose(True)

if __name__=='__main__':
  app = NSApplication.sharedApplication()
  app.activateIgnoringOtherApps_(True)
  app.setDelegate_(MyAppDelegate.create())
  AppHelper.runEventLoop()
