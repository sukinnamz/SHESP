import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
app = Flask(__name__)

mqttc=mqtt.Client()
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

mqttc1=mqtt.Client()
mqttc1.connect("localhost",1883,60)
mqttc1.loop_start()

mqttc2=mqtt.Client()
mqttc2.connect("localhost",1883,60)
mqttc2.loop_start()

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   0 : {'name' : 'Lampu Teras', 'board' : 'esp8266', 'topic' : 'esp8266/0', 'state' : 'False'}
   }
pins1 = {
   0 : {'name' : 'Lampu Ruang  Tamu', 'board' : 'esp8266_2', 'topic' : 'esp8266_2/0', 'state' : 'False'}
   }
pins2 = {
   0 : {'name' : 'Lampu Taman', 'board' : 'esp8266_3', 'topic' : 'esp8266_3/0', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:

templateData = {
   'pins' : pins,
   'pins1' : pins1,
   'pins2' : pins2
   }

@app.route("/")
def main():
   return render_template('main.html', **templateData)


@app.route("/<board>/<changePin>/<action>")
def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
#ESP 1
   if action == "1" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"0")
      pins[changePin]['state'] = 'True'
      print("off")

   if action == "0" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"1")
      pins[changePin]['state'] = 'False'
#ESP 2
   if action == "1" and board == 'esp8266_2':
      mqttc1.publish(pins1[changePin]['topic'],"0")
      pins1[changePin]['state'] = 'True'
      print("off")

   if action == "0" and board == 'esp8266_2':
      mqttc1.publish(pins1[changePin]['topic'],"1")
      pins1[changePin]['state'] = 'False'
#ESP 3
   if action == "1" and board == 'esp8266_3':
      mqttc2.publish(pins2[changePin]['topic'],"0")
      pins2[changePin]['state'] = 'True'
      print("off")

   if action == "0" and board == 'esp8266_3':
      mqttc2.publish(pins2[changePin]['topic'],"1")
      pins2[changePin]['state'] = 'False'

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins,
      'pins1' : pins1,
      'pins2' : pins2
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='192.168.56.15', port=8181)
