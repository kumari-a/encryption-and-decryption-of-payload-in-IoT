#importing imprtant libaries
#importing client
import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
import time

#function to get log information
def on_log(client, userdata, level , buf):
    print('log : ',buf)

#function to check if broker is connected
def on_connect(client,userdata,flags,rc):
    if rc==0:
        client.connected_flag=True
        print('connected ok')
    else:
        print('bad connection returned to code =', rc)
        client.loop_stop()

#function to check the disconnect code
def on_disconnect(client,userdata,flags,rc = 0):
    print('disconnected result code',str(rc)) 

#function to execute when payload is received
def on_message(client,userdata,message):
    print('received payload',message.payload)
    #decrypting the message received
    decrypted_message = cipher.decrypt(encrypted_message)
    #print the message
    print("message received " ,str(decrypted_message.decode("utf-8")))
    #printing thr topic
    print("message topic=",message.topic)
    #printing the QoS
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

#called when a message is published
def on_publish(client,userdata,mid):
    print('IN on_pub callback mid = ',mid)

#checking for subscription
def on_subscribe(client,userdata,mid,granted_qos):
    print('subscribed')

#when a client wants to reset the connection and subscription
def reset():
    ret=client.publish("house/bulbs/bulb1","",0,True)


#defining broker    
broker='broker.hivemq.com'
mqtt.Client.connected_flag=False
#creating client instance
client = mqtt.Client("python1")

#binding callback functions
client.on_connect=on_connect
client.on_disconnect = on_disconnect
client.on_log=on_log
client.on_message=on_message
client.on_publish=on_publish
client.on_subscribe=on_subscribe
client.reset=reset

#generting a key for encryption and decryption
cipher_key= Fernet.generate_key()
cipher = Fernet(cipher_key)

#message in bytes for encryption
message=b'hello there'
#encrypting the message
encrypted_message = cipher.encrypt(message)
#converting the cipher text into string
out_message=encrypted_message.decode()

print('connecting to broker : ',broker)
#connecting to broker
client.connect(broker)
#starting the loop
client.loop_start()

#waiting till the client is not connected
while not client.connected_flag:
    print('In wait loop')
    time.sleep(1)

time.sleep(3)
#subscribing to a topic
client.subscribe("house/bulbs/bulb1")
#publishing a topic
client.publish("house/bulbs/bulb1",out_message)

time.sleep(2)
#ending the loop
client.loop_stop()
#disconnect from broker
client.disconnect() 
