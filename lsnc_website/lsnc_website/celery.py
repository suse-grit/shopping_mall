import os
from celery import Celery
from django.conf import settings

# 为celery设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsnc_website.settings')
# 创建应用
app = Celery('email_celery')
# 配置应用
app.conf.update(
    # 配置broker
    BROKER_URL='redis://:@127.0.0.1:6379/10'
)
# 设置app自动加载任务
app.autodiscover_tasks(settings.INSTALLED_APPS)

# 执行celery,将django中的视图某部分函数异步化执行,更快给客户端响应
# ~/gmy/lsnc168/lsnc_website$ celery -A lsnc_website worker -l info
