# ttlock-docker

A restful API for TT lock; handles access tokens and dates

Requires gateway and uses TT lock API 

1) Create an application here: <a href="https://open.ttlock.com/manager">https://open.ttlock.com/manager</a>
<br>2) Register a user in the application - returns a prefixed user that you can add to your lock

```
curl --location -g --request POST 'https://euapi.ttlock.com/v3/user/register' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'clientId=your id' \
--data-urlencode 'client=your secret' \
--data-urlencode 'username=lockuser' \
--data-urlencode 'password=your application users password md5 hashed' \
--data-urlencode 'date=1650909361599'
```

<a href="https://currentmillis.com">https://currentmillis.com</a> - get the current date
<br>echo "password" | md5 - md5 hash password

3) Add your new prefixed user to your lock in the TT lock app
<br>4) Download docker image: <a href="https://hub.docker.com/r/stevendodd/ttlock">https://hub.docker.com/r/stevendodd/ttlock</a>
<br>5) Create a Docker container

```
docker run \
-e CLIENTID='your id' \
-e CLIENTSECRET='your secret' \
-e LOCKID='your lock id' \
-e USER='your prefixed application user' \
-e PASSWORD='your application users password md5 hashed' \
-p 5000:5000 stevendodd/ttlock
```

6) Add the following sensor and rest command to configuration.yaml in home assistant

<img src="https://community-assets.home-assistant.io/original/4X/8/5/b/85b1d906b54557dd772ced7533c7140b49738bb3.png">

```
rest:
  - scan_interval: 60
    resource: http://192.168.1.100:5000/123
    sensor:
      - name: "Front Door Lock"
        value_template: "OK"
        json_attributes:
          - "autoLockTime"
          - "electricQuantity"
          - "firmwareRevision"
          - "hardwareRevision"
          - "lockAlias"
          - "modelNum"
          - "passageMode"
          - "passageModeAutoUnlock"
          - "soundVolume"
          - "tamperAlert"

  - scan_interval: 60
    resource: http://192.168.1.100:5000/123/getstatus
    sensor:
      - name: "Front Door ttlock Status"
        value_template: "{{ value_json.state }}"
        unique_id: frontdoor_ttlock_status
        json_attributes:
          - "sensorState"
          - "state"


rest_command:
  unlock_front_door:
    url: "http://192.168.1.100:5000/123/unlock"
    method: get
  lock_front_door:
    url: "http://192.168.1.100:5000/123/lock"
    method: get

lock: 
  - platform: template
    name: Front Door
    value_template: "{{ state_attr('sensor.frontdoor_ttlock_status', 'state') | int(0) != 1 }}"
    optimistic: true
    lock: 
      - service: rest_command.lock_front_door
    unlock: 
      - service: rest_command.unlock_front_door
```
