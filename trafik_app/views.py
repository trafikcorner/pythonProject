from django.shortcuts import render, redirect
from .odbe.odbeebetu import *
from .odbe.odbeimport import *
from .odbe.odbeexport import *
from .odbe.odberendeles import *

from .cocacola.cckvexport import *
from .cocacola.ccorderstemplateimport import *
from .cocacola.ccrkexport import *

from datetime import date
from django.contrib import messages

from .models import odberkkv

from django.contrib import messages


def index(request):
    # template = loader.get_template('trafik_app/odbe.html')
    # return HttpResponse(template.render())
    return render(request, 'trafik_app/index.html')
def odbe(request):
    return render(request, "trafik_app/odbe.html")

def odbeebetu(request):
    # ODBE E betűs szótár betöltése
    url = 'http://cleaneffect.hu/ODBE_betolt.php'
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    conext = {'szotar' : data}

    # OK gomb - File kiválasztva - Raktárkészlet excelbe exportálja az "E" betűs NDN-eket
    if 'okGomb' in request.POST:
        odbeeexport(request.FILES['filenev'])
    return render(request, "trafik_app/odbeebetu.html", conext)

def odbeimport(request):
    # --- Utolsó RK dátumának betöltése ---
    url = 'http://cleaneffect.hu/ODBE_rk_datum.php'
    with urllib.request.urlopen(url) as url:
        utolsoRKDatum = json.loads(url.read().decode())
    if request.method == "POST": # KészletváltozásInfo és KV törlés
        if 'datumGomb' in request.POST:
            url = 'http://cleaneffect.hu/ODBE_torles.php'
            x = requests.post(url, data=request.POST['datumGomb'])
        if 'kvimport' in request.POST: # --- Csak akkor ha létezik, különben hiba
            temp_date = datetime.strptime(utolsoRKDatum[0]['datum'], "%Y-%m-%d").date()
            if temp_date < date.today():
                messages.error(request, 'Nincs mai raktárkészlet importálva !!!')
            else:
                odbekvimport(request.FILES['filenev'], request.POST['datumkezdet'], request.POST['megjegyzes'])
        if 'rkimport' in request.POST:
            odberkimport(request.FILES['filenev'])
        if 'odbeuresimport' in request.POST:
            odbeureslistaimport(request.FILES['filenev'])

    context = {'kvinfo' : odbekvinfobetolt(), 'rkinfo': utolsoRKDatum[0]['datum']} # Betölti a készletválozások dátumát, megjegyzést
    return render(request, "trafik_app/odbeimport.html", context)

def cocacola(request):
    print("Coca Cola")
    if 'cckvexport' in request.POST:
        cckvexport()
    if 'ccexcelimport' in request.POST:
        ccotimport()
    if 'ccrkexport' in request.POST:
        ccrkexport_otbe()

    return render(request, "trafik_app/cocacola.html")

def odbeexport(request):
    url = 'http://cleaneffect.hu/ODBE_rk_datum.php'
    with urllib.request.urlopen(url) as url:
        datum = json.loads(url.read().decode())
    current_date = date.today().strftime("%Y-%m-%d") # Mai dátum


    if 'OKButton' in request.POST:
        if request.POST['OKButton'] == 'KV':
            kvexporttoxls(request.FILES['filenev'])
            # if datum[0]['datum'] < current_date: # Ha nincs a jelenlegi RK importálva, akkor hiba
            #     messages.info(request, 'Hiba! Nincs friss raktárkészlet importálva!')
            # else: # Ha van jelenlegi RK, akkor exportája a készletváltozásokat
            #     kvexporttoxls(request.FILES['filenev'])
        if request.POST['OKButton'] == 'RK':
            print('RK export')
            rkexportotxls(request.FILES['filenev'])
    return render(request, "trafik_app/odbeexport.html")





def odberendeles(request):
    # ----- Beszállítók kigyűjtése a menühöz -----
    context = {}

    #url = 'http://cleaneffect.hu/ODBE_odbe_rk_betolt.php'
    url = 'http://cleaneffect.hu/test.php'
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())

    odberkkv.objects.all().delete()  # Model adatait törli

    # for adat in data:
    #     ndn = adat['ndn']
    #     megnevezes = adat['megnevezes']
    #     gyarto = adat['gyarto']
    #     kategoria = adat['kategoria']
    #     rendeles = adat['rendeles']
    #     raktarkeszlet = adat['raktarkeszlet']
    #     cikkszam = adat['cikkszam']
    #     kv0 = adat['kv0']
    #     kv1 = adat['kv1']
    #     kv2 = adat['kv2']
    #     kv3 = adat['kv3']
    #     odberkkv.objects.create(
    #         ndn=ndn,
    #         megnevezes=megnevezes,
    #         gyarto=gyarto,
    #         kategoria=kategoria,
    #         rendeles=rendeles,
    #         raktarkeszlet=raktarkeszlet,
    #         cikkszam=cikkszam,
    #         kv0=kv0,
    #         kv1=kv1,
    #         kv2=kv2,
    #         kv3=kv3
    #     )

    gyartok = (odbeRendeles(odberkkv).szallitok())
    #context = {"gyartok" : gyartok, "data" : odberkkv.objects.all().values()}
    context = {"gyartok": gyartok, "data": data}

    return render(request, "trafik_app/odberendeles.html", context)

