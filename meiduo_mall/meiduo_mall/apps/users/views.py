from django.shortcuts import render
from users.models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from meiduo_mall.utils.exceptions import exception_handler
from random import randint
from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP
from rest_framework.response import Response
from threading import Thread
from celery_tasks.sms.tasks import send_sms_code
# Create your views here.


# def send_sms_code(mobile, sms_code):
#     ccp = CCP()
#     ccp.send_template_sms(mobile, [sms_code, '5'], 1)


class SMS_CODEView(APIView):

    # 短信验证码
    def get(self, request, mobile):
        # 1.获取前端传递的手机号,路径中进行正则匹配
        # 判断前端发送请求的时间间隔 60s
        # 建立链接redis的对象
        conn = get_redis_connection('sms_code')
        flag = conn.get('sms_code_flag_%s' % mobile)
        if flag:
            return Response({'error': '请求过于频繁'}, status=400)
        # 2.生成短信验证码
        sms_code = '%06d' % randint(0, 999999)
        # 3.保存验证码到缓存中
            # 建立链接redis对象
        conn = get_redis_connection('sms_code')
        # string类型写入
        # setex三个参数,第一个参数是key值,第二个是有效期,第三个是value值
        # 常规用法
        # conn.setex('sms_code_%s'%mobile, 300, sms_code)
        # conn.setex('sms_code_flag_%s' % mobile, 60, 1)
        # 管道用法
        pl = conn.pipeline()
        pl.setex('sms_code_%s'%mobile, 300, sms_code)
        pl.setex('sms_code_flag_%s' % mobile, 60, 1)
        # 连接redis缓存，传入写入指令
        pl.execute()
        # 4.发送短信
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, '5'], 1)
        # 使用线程发送短信
        # t = Thread(target='send_sms_code', kwargs={'mobile': mobile, 'sms_code': sms_code})
        # t.start()
        # t.join()
        # 使用celery发送短信
        send_sms_code.delay(mobile, sms_code)
        # 5.结果返回
        return Response({'message': 'ok'})


class UserNameView(APIView):
    def get(self, request, username):
        # 1、获取前端数据，正则就匹配数据
        # 2、根据用户名查询用户对象数量
        count = User.objects.filter(username=username).count()
        # 3、返回对象数量[count]，前端会自动判断存在不存在
        return Response(
            {
                'count': count,
            }
        )


class MobileView(APIView):
    def get(self, request, mobile):
        # 1、获取前端数据，正则就匹配数据
        # 2、根据用户名查询用户对象数量
        count = User.objects.filter(mobile=mobile).count()
        # 3、返回对象数量[count]，前端会自动判断存在不存在
        return Response(
            {
                'count': count,
            }
        )











