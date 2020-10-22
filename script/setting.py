import time

#获取当前系统日期
now_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
url = "http://172.16.10.3/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
username = "Admin"
password = "zabbix"
hostfile = "script/ip.txt"
starttime = "%s 00:00:00" % (now_date)
stoptime = "%s 17:30:00" % (now_date)