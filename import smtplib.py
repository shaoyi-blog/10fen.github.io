import smtplib
import sys
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sender_email = "weather_warning@outlook.com"
sender_password = "weatherWarning"
receiver_email = "1412504071@qq.com"

weather_location="北京市朝阳区望京"

GEO_API_URL = "https://restapi.amap.com/v3/geocode/geo?address=%s&output=json&key=2cbe1a5486439c1bc294e14e14f93064" %(weather_location)

# 发起GET请求并获取API的响应
response = requests.get(GEO_API_URL)
# 解析JSON结果
data = response.json()
# 获取目标数据
geo_location = data['geocodes'][0]['location']
# 打印结果


# 发起GET请求并获取API的响应
response = requests.get("https://api.caiyunapp.com/v2/Y2FpeXVuIGFwaSB3ZWI/%s/forecast.jsonp?hourlysteps=120" %(geo_location)) 
data = response.json()
# 获取目标数据
weather_desc = data['result']['hourly']['description']

today_has_rain = False 
if('雨' in weather_desc.split('明天')[0]):
    today_has_rain = True

#  如果没有雨，直接退出即可
if not today_has_rain:
    pass
    # sys.exit(0) 


# 有雨时，发出推送


subject = "降雨预警"

# 创建MIMEMultipart对象
msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

# 创建HTML内容
html_content = """
<html>
<head>
  <title>降雨预警</title>
</head>
<body>
  <p>今天有雨🌧，出门记得带伞☔️哦<br>%s<br>详情：</p>
  <a href="https://caiyunapp.com/wx_share/?#%s">点我查看天气详情<br>默认展示当前2小时天气，点击右侧空气图标可看未来一段时间天气</a>
</body>
</html>
""" %(weather_desc
      ,geo_location
      )

# 创建HTML邮件内容
html_part = MIMEText(html_content, 'html')
msg.attach(html_part)

# 连接到SMTP服务器
smtp_server = "smtp.office365.com"
smtp_port = 587

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, sender_password)

# 发送邮件
server.sendmail(sender_email, receiver_email, msg.as_string())
server.quit()


