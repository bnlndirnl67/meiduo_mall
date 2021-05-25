from django.shortcuts import render
from users.models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from meiduo_mall.utils.exceptions import exception_handler
from random import randint
from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP
from rest_framework.response import Response
# Create your views here.


class SMS_CODEView(APIView):

    # 短信验证码
    def get(self, request, mobile):
        #1.获取前端传递的手机号,路径中进行正则匹配
        #2.生成短信验证码
        sms_code = '%06d' % randint(0, 999999)
        #3.保存验证码到缓存中
            # 建立链接redis对象
        conn = get_redis_connection('sms_code')
        # string类型写入
        # setex三个参数,第一个参数是key值,第二个是有效期,第三个是value值
        conn.setex('sms_code_%s'%mobile, 300, sms_code)
        #4.发送短信
        ccp = CCP()
        ccp.send_template_sms(mobile, [sms_code, '5'], 1)
        #5.结果返回
        return Response({'message':'ok'})