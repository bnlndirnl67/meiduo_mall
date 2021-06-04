from meiduo_mall.libs.yuntongxun.sms import CCP
# 导入celery应用
from celery_tasks.main import app

# 发送短信方法
@app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, '5'], 1)