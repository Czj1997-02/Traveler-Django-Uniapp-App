from django.apps import AppConfig
import os
 
default_app_config = 'blog.BlogConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]
 
class BlogConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '帖子模块'