from script.setting import *
import requests,json, time

def get_token():
    #获取Token
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password
        },
        "id": 0
    }
    r = requests.post(url, headers=header, data=json.dumps(data))
    auth = json.loads(r.text)
    return auth["result"]

def get_item(token,host,itemkey):
    #获取ItemID
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "host": host,
            "search": {
                "key_": itemkey
            },
        },
        "auth": token,
        "id": 1
    }
    request = requests.post(url,data=json.dumps(data),headers=header)
    dict = json.loads(request.content)
    return dict['result'][0]['itemid']

def get_data(token,itemid, start, stop):
    #获取Item值
    data = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": "extend",
            "itemids": itemid,
            "history": 0,
            "time_from": start,
            "time_till": stop,
        },
        "id": 2,
        "auth": token,
    }
    request = requests.post(url, headers=header, data=json.dumps(data))
    dict = json.loads(request.content)
    return dict['result']

def timecovert(stringtime):
    #转换时间
    timeArray = time.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def dump_cpu():
    start = timecovert(starttime)
    stop = timecovert(stoptime)
    token = get_token()

    datafile = "data/01cpuinfo.txt"
    fdata = open(datafile, 'w')
    with open(hostfile, "r") as f:
        for ips in f.readlines():
            host = ips.replace('\n', '').strip()
            # try:
            #     # 兼容Linux System CPU监控项
            #     itemkey = "system.cpu.util[,idle]"
            #     itemid = get_item(token, host, itemkey)
            # except IndexError as e:
            #     # 兼容Windows System CPU监控项
            #     itemkey = "system.cpu.load[percpu,avg1]"
            #     itemid = get_item(token, host, itemkey)
            itemkey = "system.cpu.util[,idle]"
            itemid = get_item(token, host, itemkey)
            data = get_data(token, itemid, start, stop)
            if data:
                valuelist = []
                for i in data:
                    valuelist.append(float(i["value"]))
                max_value = max(valuelist)
                fdata.write(str(round(max_value, 2)) + '\n')
                print (host,max_value)
    fdata.close()

def dump_memory():
    start = timecovert(starttime)
    stop = timecovert(stoptime)
    token = get_token()

    datafile = "data/02memoryinfo.txt"
    fdata = open(datafile, 'w')
    with open(hostfile, "r") as f:
        for ips in f.readlines():
            host = ips.replace('\n', '').strip()
            # try:
            #     # 兼容Linux System CPU监控项
            #     itemkey = "vm.memory.size[pavailable]"
            #     itemid = get_item(token, host, itemkey)
            # except IndexError as e:
            #     # 兼容Windows System CPU监控项
            #     itemkey = "vm.vmemory.size[pavailable]"
            #     itemid = get_item(token, host, itemkey)
            itemkey = "vm.memory.size[pavailable]"
            itemid = get_item(token, host, itemkey)
            data = get_data(token, itemid, start, stop)
            if data:
                valuelist = []
                for i in data:
                    valuelist.append(float(i["value"]))
                max_value = max(valuelist)
                fdata.write(str(round(max_value, 2)) + '\n')
                print (host,max_value)
    fdata.close()

def dump_disk():
    start = timecovert(starttime)
    stop = timecovert(stoptime)
    token = get_token()

    datafile = "data/03diskinfo.txt"
    fdata = open(datafile, 'w')
    with open(hostfile, "r") as f:
        for ips in f.readlines():
            host = ips.replace('\n', '').strip()
            try:
                # 部分Linux节点有"/data"目录
                itemkey = "vfs.fs.size[/data,pfree]"
                itemid = get_item(token, host, itemkey)
            except IndexError as e:
                # 部分Linux节点没有"/data"目录，故仅监控"/"目录
                itemkey = "vfs.fs.size[/,pfree]"
                itemid = get_item(token, host, itemkey)
            data = get_data(token, itemid, start, stop)
            if data:
                valuelist = []
                for i in data:
                    valuelist.append(float(i["value"]))
                max_value = max(valuelist)
                fdata.write(str(round(max_value, 2)) + '\n')
                print (host,max_value)
    fdata.close()