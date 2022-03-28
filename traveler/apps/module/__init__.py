from django.apps import AppConfig
import os
 
default_app_config = 'module.ModuleConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]
 
class ModuleConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '菜单模块'