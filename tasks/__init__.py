from celery import Celery

app = Celery('project')  # 创建 Celery 实例
app.config_from_object('tasks.config')  # 加载配置模块
