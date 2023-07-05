import json, sys, os

if len(sys.argv) <1:
	print('Please provide a JSON filepath to convert from')
	exit()
filename = sys.argv[1]
automation_devices = {}
proxy_devices = {}
automation_devices['Broker'] ={}
automation_devices['Broker']['UID'] = 'mqtt:broker:broker'
automation_devices['Broker']['Label'] = 'MQTTBroker'
automation_devices['Broker']['thingTypeUID'] = 'mqtt:broker'
automation_devices['Broker']['configuration'] ={}
automation_devices['Broker']['configuration']['lwtQos'] = 0
automation_devices['Broker']['configuration']['publickeypin']=False
automation_devices['Broker']['configuration']['keepAlive']= 60
automation_devices['Broker']['configuration']['clientID']='Upstream_automation'
automation_devices['Broker']['configuration']['secure']='true'
automation_devices['Broker']['configuration']['certificatepin']=False
automation_devices['Broker']['configuration']['password']='parapet'
automation_devices['Broker']['configuration']['qos']=0
automation_devices['Broker']['configuration']['reconnectTime']=30000
automation_devices['Broker']['configuration']['port']=1883
automation_devices['Broker']['configuration']['host']='192.168.0.51'
automation_devices['Broker']['configuration']['lwtRetain']=True
automation_devices['Broker']['configuration']['username']='parapet'
automation_devices['Broker']['configuration']['enableDiscovery']=True
proxy_devices['Broker'] ={}
proxy_devices['Broker']['UID'] = 'mqtt:broker:broker'
proxy_devices['Broker']['Label'] = 'MQTTBroker'
proxy_devices['Broker']['thingTypeUID'] = 'mqtt:broker'
proxy_devices['Broker']['configuration'] ={}
proxy_devices['Broker']['configuration']['lwtQos'] = 0
proxy_devices['Broker']['configuration']['publickeypin']=False
proxy_devices['Broker']['configuration']['keepAlive']= 60
proxy_devices['Broker']['configuration']['clientID']='PARAPET_Proxy'
proxy_devices['Broker']['configuration']['secure']='true'
proxy_devices['Broker']['configuration']['certificatepin']=False
proxy_devices['Broker']['configuration']['password']='parapet'
proxy_devices['Broker']['configuration']['qos']=0
proxy_devices['Broker']['configuration']['reconnectTime']=30000
proxy_devices['Broker']['configuration']['port']=1883
proxy_devices['Broker']['configuration']['host']='192.168.0.51'
proxy_devices['Broker']['configuration']['lwtRetain']='true'
proxy_devices['Broker']['configuration']['username']='parapet'
proxy_devices['Broker']['configuration']['enableDiscovery']=True
with open(filename,'r') as data_file:
	data = json.load(data_file)
	device_data = data['Devices']
	for dev_name in device_data.keys():
		automation_device = {}
		proxy_device = {}
		automation_device['UID'] = 'mqtt:topic:broker:'+dev_name
		automation_device['label']=dev_name
		automation_device['thingTypeUID']='mqtt:topic'
		automation_device['configuration']={}
		automation_device['bridgeUID']='mqtt:broker:broker'
		automation_device['channels']={}
		for device_item in device_data[dev_name].keys():
			
			automation_device['channels'][device_item] = {}
			automation_device['channels'][device_item]['id'] = device_item
			automation_device['channels'][device_item]['label'] = device_item
			channelTypeUID = ''
			configuration = {}
			dev_n = dev_name.replace(' ','')
			if 'bool' in device_item:
				channelTypeUID = 'mqtt:switch'
				if 'State' in dev_name:
					# configuration['commandTopic']=dev_name+'/'+device_item
					configuration['stateTopic']=dev_n+'/'+device_item
				else:
					configuration['commandTopic']=dev_n+'/'+device_item+'/'+'set'
					configuration['stateTopic']=dev_n+'/'+device_item
				configuration['off']="false"
				configuration['on']="true"
			elif 'str' in device_item:
				channelTypeUID = 'mqtt:string'
				if 'State' in dev_name:
					# configuration['commandTopic']=dev_name+'/'+device_item
					configuration['stateTopic']=dev_n+'/'+device_item
				else:
					configuration['commandTopic']=dev_n+'/'+device_item+'/'+'set'
					configuration['stateTopic']=dev_n+'/'+device_item
				configuration['formatBeforePublish']='%s'
			elif 'int' in device_item:
				channelTypeUID = 'mqtt:dimmer'
				if 'State' in dev_name:
					# configuration['commandTopic']=dev_name+'/'+device_item
					configuration['stateTopic']=dev_n+'/'+device_item
				else:
					configuration['commandTopic']=dev_n+'/'+device_item+'/'+'set'
					configuration['stateTopic']=dev_n+'/'+device_item
				configuration['formatBeforePublish']='%d'
				configuration['min'] = 0
				configuration['max'] = 100
			configuration['qos'] =0
			configuration['postCommand']=True
			configuration['retained']=False
			automation_device['channels'][device_item]['channelTypeUID']=channelTypeUID
			automation_device['channels'][device_item]['configuration']=configuration
		proxy_device['UID'] = 'mqtt:topic:broker:'+dev_n
		proxy_device['label']=dev_name
		proxy_device['thingTypeUID']='mqtt:topic'
		proxy_device['configuration']={}
		proxy_device['bridgeUID']='mqtt:broker:broker'
		proxy_device['channels']={}
		for device_item in device_data[dev_name].keys():
			proxy_device['channels'][device_item] = {}
			proxy_device['channels'][device_item]['id'] = device_item
			proxy_device['channels'][device_item]['label'] = device_item
			channelTypeUID = ''
			configuration = {}
			dev_n = dev_name.replace(' ','')
			if 'bool' in device_item:
				channelTypeUID = 'mqtt:switch'
				if 'State' in dev_name:
					# configuration['commandTopic']=dev_name+'/'+device_item
					configuration['commandTopic']=dev_n+'/'+device_item
				else:
					configuration['stateTopic']=dev_n+'/'+device_item+'/'+'set'
					configuration['commandTopic']=dev_n+'/'+device_item
				configuration['off']="false"
				configuration['on']="true"
			elif 'str' in device_item:
				channelTypeUID = 'mqtt:string'
				if 'State' in dev_name:
					# configuration['commandTopic']=dev_name+'/'+device_item
					configuration['commandTopic']=dev_n+'/'+device_item
				else:
					configuration['stateTopic']=dev_n+'/'+device_item+'/'+'set'
					configuration['commandTopic']=dev_n+'/'+device_item
				configuration['formatBeforePublish']='%s'
			elif 'int' in device_item:
				channelTypeUID = 'mqtt:dimmer'
				if 'State' in dev_name:
					# configuration['commandTopic']=dev_name+'/'+device_item
					configuration['commandTopic']=dev_n+'/'+device_item
				else:
					configuration['stateTopic']=dev_n+'/'+device_item+'/'+'set'
					configuration['commandTopic']=dev_n+'/'+device_item
				configuration['formatBeforePublish']='%d'
				configuration['min'] = 0
				configuration['max'] = 100
			configuration['qos'] =0
			configuration['postCommand']=True
			configuration['retained']=False
			proxy_device['channels'][device_item]['channelTypeUID']=channelTypeUID
			proxy_device['channels'][device_item]['configuration']=configuration
		automation_devices[dev_name] = automation_device
		proxy_devices[dev_name] = proxy_device
# write things file

things_filename = filename.replace('.json','.things')
