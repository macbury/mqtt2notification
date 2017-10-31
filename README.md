# Install
Download newest version from https://github.com/macbury/mqtt2notification/releases and place it in Applications directory

# How it works
https://www.youtube.com/watch?v=JfGdwLK64co&feature=youtu.be

# Mqtt message format
Publish valid json to mqtt topic:
```json
{ "title": "Title of notification", "message": "Content of message" }
```

# Integrating with HomeAssistant
Ensure that you have https://home-assistant.io/components/mqtt/ configured!
Copy `home-assistant/custom_components/notify/mqtt2notification.py` to your `<config-dir>/custom_components/notify/` directory and add **mqtt2notification** platform in `<config>/configuration.yaml` file:

``` yaml
mqtt:

notify:
  - name: mqtt2notification
    platform: mqtt2notification
    topic: living_room/notifications
```

# Build
```shell
pip install -r requirements.txt
bin/build
bin/run
```

# Caveats
To enable actions on the notification (the buttons that allow the user to select an option), open System Preferences > Notifications, select mqtt2notification in the sidebar, and select the "Alerts" alert style. 
![Enable alerts in System Preferences](assets/System_prefs.png)

# Icons from

https://www.iconfinder.com/icons/2246841/bell_notification_one_notification_tiwtter_icon#size=128
https://www.iconfinder.com/icons/2236309/alert_bell_notification_twitter_icon#size=128
