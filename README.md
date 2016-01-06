# TweetRPiStatus
Tweeting Raspberry Pi status: 
- Hostname
- CPUTemp
- CPU Usage
- Free Diskspace
- Free Memory

For now the program expects a twitter.conf file in /etc/init
An example file is added,please generate your own keys and add them, after which you can add the file

The program also works when used in cron (hence the definition of TERM)
