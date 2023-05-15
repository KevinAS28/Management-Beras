from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.urls import reverse
from django.db.models import Max
from django.db.models.query import QuerySet
from django.urls import resolve

# from cost_calculator.row_items import row_items
from django.core.handlers.wsgi import WSGIRequest
import cost_calculator.models as models
from datetime import date
import calendar

import json
import math
import re
import math
import traceback


item_inputs = ['Jumlah unit','Harga per unit', 'Biaya total', '_']


class CostItemToday:
    def __init__(self, the_date):
        self.cd = the_date
    
    def get(self, name=None, name_id=None) -> models.CostItem:
        kwargs = {'name': name} if name_id is None else {'name_id': name_id}
        return models.CostItem.objects.get(the_date=self.cd, **kwargs)

    def normal_multiply(self, name_id, inputs_per_date):
        cost_item = self.get(name_id=name_id)
        cost_item.unit_count = int(inputs_per_date[f'numinput_jumlah_unit_{name_id}'])
        cost_item.unit_price = int(inputs_per_date[f'numinput_harga_per_unit_{name_id}'])
        cost_item.save()            
        return cost_item  
    
    def semi_automatic_multiply(self, name_id, inputs_per_date, modified_inputs_per_date):
        try:
            cost_item = self.get(name_id=name_id)
        except Exception as e:
            print(str(e))
            print(traceback)
            raise Exception(f'no {name_id}')
        if f'numinput_jumlah_unit_{name_id}' in modified_inputs_per_date:
            cost_item.unit_count = int(inputs_per_date[f'numinput_jumlah_unit_{name_id}'])
        if f'numinput_harga_per_unit_{name_id}' in modified_inputs_per_date:
            cost_item.unit_price = int(inputs_per_date[f'numinput_harga_per_unit_{name_id}'])        
        cost_item.save()
        return cost_item

class OutcomeItemToday:
    
    def __init__(self, the_date):
        self.cd = the_date
    
    def get(self, name=None, name_id=None) -> models.CostItem:
        kwargs = {'name': name} if name_id is None else {'name_id': name_id}
        return models.OutcomeItem.objects.get(the_date=self.cd, **kwargs)
    


def calculate_outcome(dates, user_inputs):
    for date_index, the_date in enumerate(dates):    
        inputs_per_date = {re.search(f'(.*)(\|{the_date.pk})', key).groups()[0]:user_inputs[key][0] for key in user_inputs if key.startswith('numinput_') and key.endswith(f'|{the_date.pk}')}
        modified_inputs_per_date = [re.search(f'(.*)(\|{the_date.pk})', key).groups()[0] for key in json.loads(user_inputs['modified_inputs'][0]) if key.endswith(f'|{the_date.pk}')]
        for key, value in inputs_per_date.items():
            if key.startswith('numinput') :
                if value=='':
                    inputs_per_date[key] = 0
                else:
                    inputs_per_date[key] = int(value)

        if models.OutcomeItem.objects.filter(the_date=the_date).count()==0:
            outcome_item_today = models.OutcomeItem(the_date=the_date, pemasukan=int(inputs_per_date['numinput_jumlah_unit_pemasukan_uang'], berat_hasil_beras=int(inputs_per_date['numinput_jumlah_unit_berat_hasil_beras']), description=user_inputs[f'desc_outcome|{the_date.pk}'][0])) 
            outcome_item_today.save()
        else:
            outcome_item_today = models.OutcomeItem.objects.get(the_date=the_date)
            outcome_item_today.pemasukan = int(inputs_per_date['numinput_jumlah_unit_pemasukan_uang'])
            outcome_item_today.berat_hasil_beras = int(inputs_per_date['numinput_jumlah_unit_berat_hasil_beras'])
            outcome_item_today.description = user_inputs[f'desc_outcome|{the_date.pk}'][0]
            outcome_item_today.save()


def calculate_costs(dates, user_inputs):
    for date_index, cost_date in enumerate(dates):
        inputs_per_date = {re.search(f'(.*)(\|{cost_date.pk})', key).groups()[0]:user_inputs[key][0] for key in user_inputs if key.startswith('numinput_') and key.endswith(f'|{cost_date.pk}')}
        modified_inputs_per_date = [re.search(f'(.*)(\|{cost_date.pk})', key).groups()[0] for key in json.loads(user_inputs['modified_inputs'][0]) if key.endswith(f'|{cost_date.pk}')]
        for key, value in inputs_per_date.items():
            if key.startswith('numinput') :
                if value=='':
                    inputs_per_date[key] = 0
                else:
                    inputs_per_date[key] = int(value)
        # print(inputs_per_date)
        
        cost_item_today = CostItemToday(the_date=cost_date)
        # print('ipd', inputs_per_date)
        # print('modified', modified_inputs_per_date)
        #check sumber padi, satu atau lebih harus diisi unit dan harganya
        sumber_padi = [
            'padi_supadi:_ke_lokasi_petani_bandar',
            'padi_supadi:_bandar_ke_pabrik',
            'padi_supadi:_petani_ke_pabrik',
            'padi_supadi:_sendiri',
            'padi_ketan:_ke_lokasi_petani_bandar',
            'padi_ketan:_bandar_ke_pabrik',
            'padi_merah:_ke_lokasi_petani_bandar',
            'padi_merah:_bandar_ke_pabrik',
            'padi_lainnya:_ke_lokasi_petani_bandar',
            'padi_lainnya:_bandar_ke_pabrik',
            'padi_lainnya:_petani_ke_pabrik',
            'padi_lainnya:_sendiri',
        ]
        total_harga_padi = {key: int(inputs_per_date[f'numinput_jumlah_unit_{key}'])*int(inputs_per_date[f'numinput_harga_per_unit_{key}']) for key in sumber_padi}

        for key,value in total_harga_padi.items():
            cost_item = cost_item_today.get(name_id=key)
            cost_item.unit_count = int(inputs_per_date[f'numinput_jumlah_unit_{key}'])
            cost_item.unit_price = int(inputs_per_date[f'numinput_harga_per_unit_{key}'])            
            cost_item.total_price = total_harga_padi[key]
            cost_item.save()
            
            
        
        if sum(total_harga_padi.values())==0:
            print('harga padi harus diisi')
        else:
            print('total_harga_padi: ', total_harga_padi)
            
        
        # Biaya solar bagi sumber padi yang butuh transportasi 
        sumber_padi_butuh_transport = [
            'padi_supadi:_ke_lokasi_petani_bandar',
            'padi_supadi:_sendiri',
            'padi_ketan:_ke_lokasi_petani_bandar',
            'padi_merah:_ke_lokasi_petani_bandar',
            'padi_lainnya:_ke_lokasi_petani_bandar',
            'padi_lainnya:_sendiri',
        ]
        total_berat_padi_butuh_transport = sum([int(inputs_per_date[f'numinput_jumlah_unit_{key}']) for key in sumber_padi_butuh_transport])
        
        cost_item_today.semi_automatic_multiply('bbm-solar_truk:_spbu', inputs_per_date, modified_inputs_per_date)        
        cost_item_today.semi_automatic_multiply('bbm-solar_l300:_spbu', inputs_per_date, modified_inputs_per_date)        

        cost_item_today.semi_automatic_multiply('bbm-solar_truk:_lainnya', inputs_per_date, modified_inputs_per_date)

        cost_item_today.semi_automatic_multiply('bbm-solar_l300:_lainnya', inputs_per_date, modified_inputs_per_date)

        
        # Karung / Plastik
        total_berat_hasil_beras = sum([cost_item_today.get(name_id=name_id_padi).unit_count for name_id_padi in sumber_padi])*0.61

        cost_item_today.semi_automatic_multiply('karung_plastik-_25kg', inputs_per_date, modified_inputs_per_date)

        cost_item_today.semi_automatic_multiply('karung_plastik-_10kg', inputs_per_date, modified_inputs_per_date)
        
        cost_item_today.semi_automatic_multiply('karung_plastik-_5kg', inputs_per_date, modified_inputs_per_date)

        cost_item_today.semi_automatic_multiply('karung_plastik-lainnya', inputs_per_date, modified_inputs_per_date)

        #Biaya pekerja bongkar di pabrik
        padi_butuh_dibongkar_name_id = [
            'padi_supadi:_ke_lokasi_petani_bandar',
            'padi_supadi:_sendiri',
            'padi_ketan:_ke_lokasi_petani_bandar',
            'padi_merah:_ke_lokasi_petani_bandar',
            'padi_lainnya:_ke_lokasi_petani_bandar',
            'padi_lainnya:_sendiri',            
        ]

        total_berat_padi_dibongkar = sum([int(inputs_per_date[f'numinput_jumlah_unit_{key}']) for key in padi_butuh_dibongkar_name_id])
        biaya_bongkar:models.CostItem = cost_item_today.get(name_id='biaya_pekerja_pabrik:_bongkar_di_pabrik')
        biaya_bongkar.unit_count = total_berat_padi_dibongkar
        biaya_bongkar.unit_price = 10
        biaya_bongkar.save()
        
        #Biaya pekerja load ke truk
        total_berat_padi = sum([int(inputs_per_date[f'numinput_jumlah_unit_{key}']) for key in sumber_padi]) #beras doang apa smua?
        biaya_load = cost_item_today.get(name_id='biaya_pekerja_pabrik:_loading_ke_alat_angkut')
        biaya_load.unit_count = total_berat_padi
        biaya_load.unit_price = 20
        biaya_load.save()

        cost_item_today.semi_automatic_multiply('biaya_pekerja_pabrik:_sopir_truck_dalam_kota', inputs_per_date, modified_inputs_per_date)
        cost_item_today.semi_automatic_multiply('biaya_pekerja_pabrik:_sopir_l300_dalam_kota', inputs_per_date, modified_inputs_per_date)
        cost_item_today.semi_automatic_multiply('biaya_pekerja_pabrik:_sopir_truck_luar_kota', inputs_per_date, modified_inputs_per_date)
        cost_item_today.semi_automatic_multiply('biaya_pekerja_pabrik:_sopir_l300_luar_kota', inputs_per_date, modified_inputs_per_date)
        cost_item_today.semi_automatic_multiply('biaya_pekerja_pabrik:_buruh_lainnya', inputs_per_date, modified_inputs_per_date)
        
        biaya_pekerja_pk = cost_item_today.get(name_id='biaya_pekerja_pabrik:_buat_pk')
        biaya_pekerja_pk.unit_count = sum([int(inputs_per_date[f'numinput_jumlah_unit_{key}']) for key in sumber_padi])
        biaya_pekerja_pk.save()

        biaya_ngarungin_huut = cost_item_today.get(name_id='biaya_pekerja_pabrik:_ngarungin_dedak_huut')
        biaya_ngarungin_huut.unit_count = int(inputs_per_date['numinput_jumlah_unit_biaya_pekerja_pabrik:_ngarungin_dedak_huut'])
        biaya_ngarungin_huut.save()

        biaya_makan_buruh_pabrik = cost_item_today.get(name_id='biaya_makan_minum:_buruh_pabrik')
        biaya_makan_buruh_pabrik.unit_count = int(inputs_per_date['numinput_jumlah_unit_biaya_makan_minum:_buruh_pabrik'])
        biaya_makan_buruh_pabrik.save()

        simple_multiply_ids = ['lumpsum_pasar:_sopir_truck', 'lumpsum_pasar:_sopir_l300', 'lumpsum_pasar:_pengawas', 'lumpsum_pasar:_buruh_pabrik', 'lumpsum_pasar:_lainnya', 'biaya_lain:_transportasi_bongkar_muatan', 'biaya_lain:_keamanan_kebersihan_air', 'biaya_lain:_perlengkapan_kerja:_pakaian_sepatu', 'biaya_lain:_perlengkapan_kerja:_masker_kerja', 'biaya_lain:_perlengkapan_kerja:_tambahan_vitamin', 'biaya_lain:_perlengkapan_kerja:_tools', 'biaya_lain:_maintenance_service_alat:_roll_mollen_1', 'biaya_lain:_maintenance_service_alat:_roll_mollen_2', 'biaya_lain:_maintenance_service_alat:_saringan_ichi_1', 'biaya_lain:_maintenance_service_alat:_saringan_ichi_2', 'biaya_lain:_maintenance_service_alat:_belting_motor', 'biaya_lain:_maintenance_service_alat:_belt_conveyor', 'biaya_lain:_maintenance_service_alat:_baut-baut', 'biaya_lain:_maintenance_service_alat:_mangkok_conveyor', 'biaya_lain:_maintenance_service_alat:_lampu-lampu', 'biaya_lain:_maintenance_service_alat:_gas_kompor', 'biaya_lain:_maintenance_service_alat:_perlengkapan_dapur', 'biaya_lain:_maintenance_service_alat:_mesin_jahit', 'biaya_lain:_maintenance_service_alat:_timbangan_duduk', 'biaya_lain:_maintenance_service_alat:_timbangan_gantung', 'biaya_lain:_maintenance_service_alat:_lain-lain', 'biaya_lain:_maintenance_service_alat:_listrik', 'biaya_lain:_maintenance_service_alat:_sparepart_kendaraan', 'biaya_lain:_parkir_l300', 'biaya_lain:_parkir_truck', 'biaya_lain:_toll_truck_l300']
        for c_id in simple_multiply_ids:
            cost_item_today.semi_automatic_multiply(c_id, inputs_per_date, modified_inputs_per_date)
        
        the_cost_date = models.Date.objects.get(pk=cost_date.pk)
        the_cost_date.description = user_inputs[f'desc_{date_index}'][0]
        the_cost_date.save()

selected_dates = list(models.Date.objects.all())
items = {'year_dates': models.Date.objects.all().values_list('year', flat=True).distinct()}

def get_calculated_data(dates_to_show):
    
    #Cost
    colspan = len(item_inputs)-1
    subcolumn_items = (item_inputs)*len(dates_to_show)
    all_items_per_date = {cd.pk: models.CostItem.objects.filter(the_date=cd, sort_order__gte=0).order_by('sort_order') for cd in dates_to_show}
    unique_items = []#models.CostItem.objects.none()
    for cd_pk in all_items_per_date: #sort by sort_order
        negative_sort_orders = models.CostItem.objects.filter(the_date=models.Date.objects.get(pk=cd_pk), sort_order=-1)
        for ci in all_items_per_date[cd_pk]:
            if not ((ci.name, ci.unit_type) in unique_items):
                # unique_items |= models.CostItem.objects.filter(pk=ci.pk)
                unique_items.extend([(c.name, c.unit_type) for c in models.CostItem.objects.filter(pk=ci.pk)])
        # all_items_per_date[cd_pk] |= negative_sort_orders
        all_items_per_date[cd_pk] = [model_to_dict(ci) for ci in all_items_per_date[cd_pk]]
    # negative_sort_orders = models.CostItem.objects.filter(cost_date__in=selected_dates, sort_order=-1).values_list('name', flat=True).distinct()
    # unique_items.extend(negative_sort_orders)
    total_price_per_date = {cd_pk: sum([i['total_price'] for i in all_items_per_date[cd_pk]]) for cd_pk in all_items_per_date}

    #Outcome
    outcomes_per_date = dict()
    for the_date in dates_to_show:
        print(the_date.date)
        outcomes_per_date[the_date.pk] = model_to_dict(models.OutcomeItem.objects.get(the_date=models.Date.objects.get(pk=the_date.pk)))        

    new_items = {'outcomes_per_date': outcomes_per_date, 'descriptions': [cd.description for cd in dates_to_show], 'total_price_per_date': total_price_per_date,'unique_items': unique_items, 'item_inputs':item_inputs, 'all_items_per_date': all_items_per_date, 'column_items':[str(i.date) + ' - ' + models.Date.indonesia_days[i.date.weekday()] for i in dates_to_show], 'subcolumn_items': subcolumn_items, 'colspan': colspan, 'all_items_per_date_str': json.dumps(all_items_per_date), 'refresh': 0}

    return new_items

def cost_calculator_daily(request: WSGIRequest):
    global selected_dates, items
    for cd in selected_dates:
        cd.refresh_from_db()

    new_items = dict()
    
    if request.method=='POST':
        # print(request.POST)
        if 'hide_date' in request.POST:
            print('hide_date')
            del selected_dates[int(request.POST['hide_date'][0])]
        if 'add_date' in request.POST:
            print('add_date')
            if request.POST['add_date']=='add_date':
                if 'add_year' in request.POST:
                    # request.session['select_new_date']
                    add_year = int(request.POST['add_year'])
                    if add_year==-1:
                        if 'selected_year' in request.session:
                            del request.session['selected_year']
                        if 'month_dates' in items:
                            del items['month_dates']
                    else:
                        request.session['selected_year'] = add_year
                        items['month_dates'] = models.Date.objects.filter(year=add_year).values_list('month', flat=True).distinct()
                if 'add_month' in request.POST:
                    add_month = int(request.POST['add_month'])
                    if (add_month==-1) or (add_year==-1):
                        if 'selected_month' in request.session:
                            del request.session['selected_month']
                        if 'day_dates' in items:
                            del items['day_dates']                
                    else:
                        request.session['selected_month'] = add_month
                        items['day_dates'] = models.Date.objects.filter(month=add_month).values_list('day', flat=True).distinct()            
                if 'add_day' in request.POST:
                    add_day = int(request.POST['add_day'])
                    if (add_day==-1) or (add_month==-1) or (add_year==-1):
                        if 'selected_day' in request.session:
                            del request.session['selected_day']             
                    else:
                        request.session['selected_day'] = add_day
                        showed_date_ids = [cd.pk for cd in selected_dates]
                        selected_dates.extend( [cd for cd in models.Date.objects.filter(year=int(request.session['selected_year']), month=int(request.session['selected_month']), day=int(request.session['selected_day'])) if not (cd.pk in showed_date_ids)] )
                        new_items['refresh'] = 1

            elif request.POST['add_date']=='today':
                today_date = date.today()
                if models.Date.objects.filter(date=today_date).count()==0:
                    old_cost_date = models.Date.objects.get(date=date(year=2023, month=5, day=1))
                    today_cost_date = models.Date()
                    today_cost_date.save()

                    old_cis = models.CostItem.objects.filter(the_date=old_cost_date)                
                    for c in old_cis:
                        c.pk = None
                        c.the_date = today_cost_date
                        c.save()
                    
                    old_outcomes = models.OutcomeItem.objects.filter(the_date=old_cost_date)
                    for c in old_outcomes:
                        c.pk = None
                        c.the_date = today_cost_date
                        c.save()
                    
                else:
                    today_cost_date = models.Date.objects.get(date=today_date)

                
                showed_dates = [c.date for c in selected_dates]
                if not (today_date in showed_dates):
                    selected_dates.append(today_cost_date)
                

        if 'button_update_data' in request.POST:
            print('update calculate')
            for cd in selected_dates:
                cd.refresh_from_db()            
            calculate_costs(selected_dates, dict(request.POST))
            calculate_outcome(selected_dates, dict(request.POST))
            new_items['refresh'] = 1
        
        items = {**items, **new_items, **get_calculated_data(selected_dates)}
        return render(request, 'cost_calculator_daily.html', items)

    elif request.method=='GET':
        if 'selected_dates' in request.GET:
            print(request.GET['selected_dates'].split(','))
            request_selected_dates = [date(year=int(i.split('-')[0]), month=int(i.split('-')[1]), day=int(i.split('-')[2])) for i in request.GET['selected_dates'].split(',')]
            # print(request_selected_dates)
            selected_dates = list(models.Date.objects.filter(date__in=request_selected_dates))
        items = {**items, **new_items, **get_calculated_data(selected_dates)}
        return render(request, 'cost_calculator_daily.html', items)
    
def cost_calculator_monthly(request: WSGIRequest):
    sumber_padi = [
            'padi_supadi:_ke_lokasi_petani_bandar',
            'padi_supadi:_bandar_ke_pabrik',
            'padi_supadi:_petani_ke_pabrik',
            'padi_supadi:_sendiri',
            'padi_ketan:_ke_lokasi_petani_bandar',
            'padi_ketan:_bandar_ke_pabrik',
            'padi_merah:_ke_lokasi_petani_bandar',
            'padi_merah:_bandar_ke_pabrik',
            'padi_lainnya:_ke_lokasi_petani_bandar',
            'padi_lainnya:_bandar_ke_pabrik',
            'padi_lainnya:_petani_ke_pabrik',
            'padi_lainnya:_sendiri',
            ]    
    if request.method=='GET':
        if (not ('month' in request.GET)) or (not ('year' in request.GET)):            
            return redirect(f"/{resolve(request.path_info).route}?month={date.today().month}&year={date.today().year}&day={date.today().day}")
        
        the_day = date(year=int(request.GET['year']), month=int(request.GET['month']), day=int(request.GET['day']))
        all_dates_this_month = list(models.Date.objects.filter(month=the_day.month).order_by('day'))
        calendar_items = []
        for the_date in all_dates_this_month:
            today_outcome = models.OutcomeItem.objects.get(the_date=the_date)
            today_costs = models.CostItem.objects.filter(the_date=the_date)
            today_cost_total = sum([i.total_price for i in today_costs])
            today_date_str = str(the_date.date)
            
            #keuntungan/rugi
            bbh = today_outcome.pemasukan - today_cost_total
            calendar_items.append({
                'title': f'BBH: Rp. {bbh}',
                'url': f'/cost_calculator/daily?selected_dates={today_date_str}',
                'start': f'{today_date_str}T00:00:00'

            })

            #pemasukan
            calendar_items.append({
                'title': f'Pemasukan: Rp. {today_outcome.pemasukan}',
                'url': f'/cost_calculator/daily?selected_dates={today_date_str}',
                'start': f'{today_date_str}T04:00:00'

            })            

            #pengeluaran
            calendar_items.append({
                'title': f'Modal: Rp. {today_cost_total}',
                'url': f'/cost_calculator/daily?selected_dates={today_date_str}',
                'start': f'{today_date_str}T08:00:00'

            })              

            #masukkan beras
            calendar_items.append({
                'title': f'Beras: Rp. {sum([i.unit_count for i in today_costs.filter(name_id__in=sumber_padi) ])} KG',
                'url': f'/cost_calculator/daily?selected_dates={today_date_str}',
                'start': f'{today_date_str}T12:00:00'

            })            

            #randemen
            calendar_items.append({
                'title': f'Randemen: Rp. {today_outcome.randemen_beras*100} %',
                'url': f'/cost_calculator/daily?selected_dates={today_date_str}',
                'start': f'{today_date_str}T16:00:00'

            })            

        monthly_outcomes = models.OutcomeItem.objects.filter(the_date__in=all_dates_this_month)
        monthly_costs = models.CostItem.objects.filter(the_date__in=all_dates_this_month)
        total_monthly_outcomes = sum([i.pemasukan for i in monthly_outcomes])
        total_monthly_costs = sum([i.total_price for i in monthly_costs])
        total_incoming_rices = sum([i.unit_count for i in monthly_costs.filter(name_id__in=sumber_padi)])
        total_randemen_beras = 100*(sum([i.randemen_beras for i in monthly_outcomes])/(len(monthly_outcomes) if len(monthly_outcomes)!=0 else 1))
        # sum([i.unit_count for i in models.CostItem.objects.filter(the_date__month=today.month, name_id__in=sumber_padi)])

        items = {
            'default_day': str(the_day),
            'calendar_items': json.dumps(calendar_items),
            'monthly_bbh': total_monthly_outcomes-total_monthly_costs,
            'total_monthly_outcomes': total_monthly_outcomes,
            'total_monthly_costs': total_monthly_costs,
            'total_incoming_rices': total_incoming_rices,
            'total_randemen_beras': total_randemen_beras,
            'current_day': the_day.day,
            'current_month': the_day.month,
            'current_year': the_day.year,
            'today_day': date.today().day,
            'today_month': date.today().month,
            'today_year': date.today().year,            
            'refresh_url': f'{request.path}'
        }

        return render(request, 'cost_calculator_monthly.html', items)
    pass
