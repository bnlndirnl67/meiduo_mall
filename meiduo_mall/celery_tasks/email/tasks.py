from celery_tasks.main import app

@app.task(name='send_email')
def send_email():
    pass


# 也可以在同一个文件里写入方法
@app.task(name='a_print')
def a_print():
    print('aaa')