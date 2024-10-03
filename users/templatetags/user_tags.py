from django import template
from constants import MENU


register = template.Library()

@register.simple_tag()
def get_menu():
    return  MENU