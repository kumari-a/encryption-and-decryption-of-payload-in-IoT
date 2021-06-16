#importing libraries
#importing client 
import paho.mqtt.client as mqtt
import time
import json
#creting dictionary to transmit over the network
brokers_out={"broker1":"192.168.1.206",
         "broker2":"test.mosquitto.org",
         "broker3":"iot.eclipse.org"
         }
print(brokers_out)
print("brokers_out is a ",type(brokers_out))
print("broker 1 address = ",brokers_out["broker1"])
# encode oject to JSON
data_out=json.dumps(brokers_out)
print("\nConverting to JSON\n")
print ("data -type ",type(data_out))
print ("data out =",data_out)

#At Receiver
print("\nReceived Data\n")
data_in=data_out
print ("\ndata in-type ",type(data_in))
print ("data in=",data_in)
#convert incoming JSON to object
brokers_in=json.loads(data_in) 
print("brokers_in is a ",type(brokers_in))
print("\n\nbroker 2 address = ",brokers_in["broker2"])
cont=input("enter to Continue")

#defining actions on receing data
def on_message(client, userdata, msg):
    topic=msg.topic
    #decoding message
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    #printing message type
    print("data Received type",type(m_decode))
    #printing data received
    print("data Received",m_decode)
    print("Converting from Json to Object")
    m_in=json.loads(m_decode)
    print(type(m_in))
    print("broker 2 address = ",m_in["broker2"])

#defining topic
topic="test/json_test"
#creating client instance
client=mqtt.Client("pythontest1")
#binding callback functions
client.on_message=on_message
print("Connecting to broker ",brokers_out["broker2"])
#connecting to broker
client.connect(brokers_out["broker2"])
#loop starts
client.loop_start()
#subscribing to topic
client.subscribe(topic)
time.sleep(3)
print("sending data")
#publishing the data
client.publish(topic,data_out)
time.sleep(10)
#ending the loop
client.loop_stop()
#disconnecting the client
client.disconnect()
