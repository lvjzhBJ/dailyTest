#coding=utf-8
import traceback
import logging
from random import Random
from django.core.mail import send_mail
from userAuth.models import EmailVerifyRecord,User
# from django.core.mail import EmailMultiAlternatives
from django.conf import settings


logger = logging.getLogger("django")  # 为loggers中定义的名称

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    try:
        email_record = EmailVerifyRecord()
        # 将给用户发的信息保存在数据库中
        code = random_str(16)
        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type
        email_record.save()

        logger.debug(email_record)
        from_email = settings.DEFAULT_FROM_EMAIL

        # 如果为注册类型
        if send_type == "register":
            email_title = "注册激活链接"
            # email_body_text = "123"
            email_body_html = "请点击下面的链接激活你的账号:http://47.93.220.141/active/{0}".format(code)
            # 发送邮件
            logger.debug(email_title)
            logger.debug(email)
            send_status = send_mail(email_title, email_body_html, from_email, [email])
            logger.debug(send_status)
            # msg = EmailMultiAlternatives(email_title,email_body_text, from_email, [email])
            #
            # msg.attach_alternative(email_body_html, "text/html")

            # send_status = msg.send()
            # logger.debug(send_status)

            if send_status:
                pass
        elif send_type == "forget":
            user=User.objects.get(email=email)
            email_title = "get pwd"
            email_body = ("pwd:"+user.password).format(code)

            send_status = send_mail(email_title, email_body, from_email, [email])
            if send_status:
                pass
    except:
        logger.debug(traceback.format_exc())