import paho.mqtt.publish as publish

publish.single("paho/IOTtest", "test", hostname="mqtt.eclipseprojects.io")