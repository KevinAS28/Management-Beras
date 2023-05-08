from django import template

register = template.Library()

@register.filter
def get_dict_item(dictionary:dict, key):
    try:
        return dictionary.get(key)
    except:
        return f'error {key}: {dictionary}'

@register.filter
def get_list_item(the_list:list, key):
    try:
        return the_list[key]
    except:
        return f'error {key}: {the_list}'

@register.filter
def get_unit_count(the_list:list, key):
    try:
        return the_list[key]['unit_count']
    except:
        return f'error {key}: {the_list}'

@register.filter
def get_unit_price(the_list:list, key):
    try:
        return the_list[key]['unit_price']
    except:
        return f'error {key}: {the_list}'

@register.filter
def get_total_price(the_list:list, key):
    try:
        return the_list[key]['total_price']
    except:
        return f'error {key}: {the_list}'

@register.filter
def get_cost_date(the_list:list, key):
    try:
        return the_list[key]['the_date']
    except:
        return f'error {key}: {the_list}'

@register.filter
def get_name_id(the_list:list, key):
    try:
        return the_list[key]['name_id']
    except:
        return f'error {key}: {the_list}'


@register.filter
def get_unit_type(the_list:list, key):
    try:
        return the_list[key]['unit_type']
    except:
        return f'error {key}: {the_list}'