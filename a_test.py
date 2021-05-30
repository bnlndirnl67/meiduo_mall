# 任务队列
broker = []

# 定义任务的方法
def a_print():
    print('aaa')
# 添加任务队列
broker.append(a_print)

# 任务执行者
def worker():
    for a in broker:
        a()