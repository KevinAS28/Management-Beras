from cost_calculator.models import *
from datetime import date

def get_costitems_sorted_order(cost_date):

    all_cost_items = dict()
    for c in CostItem.objects.filter(the_date=cost_date):
        if not (c.sort_order) in all_cost_items:
            all_cost_items[c.sort_order] = [c]
        else:
            all_cost_items[c.sort_order].append(c)

    cost_items_sorted = [c for sort_order in sorted(all_cost_items) for c in all_cost_items[sort_order]]
    return cost_items_sorted

def print_cost_items(cost_items):
    for i, c in enumerate(cost_items):
        fields = [i, c.pk, c.sort_order, c.name_id, c.name, c.total_price]
        print(' | '.join([str(_) for _ in fields]))

def add_sort_index(cost_items, increment, start_index, stop_index):
    for c in cost_items[start_index:stop_index]:
        c.sort_order += increment
        c.save()

def clone_date(cost_date_new, cost_date_old=date(year=2023, month=5, day=1)):
    if Date.objects.filter(date=cost_date_new).count()==0:
        old_cost_date = Date.objects.get(date=date(year=2023, month=5, day=1))
        today_cost_date = Date(date=date)
        today_cost_date.save()

        old_cis = CostItem.objects.filter(the_date=old_cost_date)                
        for c in old_cis:
            c.pk = None
            c.the_date = today_cost_date
            c.save()
        
        old_outcomes = OutcomeItem.objects.filter(the_date=old_cost_date)
        for c in old_outcomes:
            c.pk = None
            c.the_date = today_cost_date
            c.save()
        
    else:
        print('Date sudah ada')
        today_cost_date = Date.objects.get(date=cost_date_new)

all_cost_dates = list(Date.objects.all())
cost_items_sorted = get_costitems_sorted_order(all_cost_dates[0])
# add_sort_index(cost_items_sorted, 1, 29, 69)
print_cost_items(cost_items_sorted)
