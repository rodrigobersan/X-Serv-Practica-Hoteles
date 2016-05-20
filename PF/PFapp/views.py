from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import urllib, datetime
from models import Alojamientos
from models import Images
from models import Comments
from models import UserSels

# Create your views here.
def main(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    offset = int(request.GET['offset'])
    comments = Comments.objects.all()
    offsets_list = range(0,len(comments)/10+1)
    comments = comments[offset*10:offset*10+10]
    xmlparse()
    usuarios = User.objects.all()
    template = get_template('main.html')
    context = ({'home': request.get_host(),
                'username': request.user.username,
                'logged': logged,
                'usuarios': usuarios,
                'offsets_list': offsets_list,
                'comments': comments})
    return HttpResponse(template.render(context))


@csrf_exempt
def alojamientos(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    offset = int(request.GET['offset'])
    if request.method == 'POST':
        filt = request.POST['filt']
    else:
        filt = request.GET['filt']
    if filt == 'None':
        alojamientos = Alojamientos.objects.all()
        offsets_list = range(0,len(alojamientos)/10+1)
        alojamientos = alojamientos[10*offset:10*offset+10]
    else:
        alojamientos = Alojamientos.objects.filter(name__contains=filt)
        offsets_list = range(0,len(alojamientos)/10+1)
        alojamientos = alojamientos[10*offset:10*offset+10]
    template = get_template('alojamientos.html')
    context = ({'home': request.get_host(),
                'path': request.get_full_path(),
                'username': request.user.username,
                'logged': logged,
                'offset': offset,
                'filt': filt,
                'offsets_list': offsets_list,
                'alojamientos': alojamientos})
    return HttpResponse(template.render(context))


@csrf_exempt
def alojamiento(request,ident):
    if request.user.is_authenticated():
        logged = True
        try:
            usersel = UserSels.objects.get(user=request.user.username,alojamiento_id=ident)
        except UserSels.DoesNotExist:
            usersel = UserSels(user=request.user.username, date = datetime.datetime.now(), alojamiento_id=ident)
            usersel.save()
    else:
        logged = False
    if request.method == 'POST':
        alojamiento = Alojamientos.objects.get(id=int(ident))
        comment = Comments(text = request.POST['comment'], date = datetime.datetime.now(), alojamiento_id = int(ident))
        comment.save()
    try:
        alojamiento = Alojamientos.objects.get(id=ident)
    except Alojamientos.DoesNotExist:
        return HttpResponse("El alojamiento al que intentas acceder no esta disponible")
    images = Images.objects.filter(alojamiento_id=ident)
    template = get_template('alojamiento.html')
    context = ({'home': request.get_host(),
                'username': request.user.username,
                'logged': logged,
                'alojamiento': alojamiento,
                'images': images})
    return HttpResponse(template.render(context))


@csrf_exempt
def usuario(request,user):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    offset = int(request.GET['offset'])
    usersels = UserSels.objects.filter(user=user)
    """if request.method == 'POST':
        if request.POST['leng'] == 'Ingles':
            #xmlparse_leng("http://www.esmadrid.com/opendata/alojamientos_v1_en.xml")
            usersels = xmlparse_leng("http://cursosweb.github.io/etc/alojamientos_en.xml",usersels)
        elif request.POST['leng'] == 'Frances':
            #xmlparse_leng("http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml")
            usersels = xmlparse_leng("http://cursosweb.github.io/etc/alojamientos_fr.xml",usersels)"""
    offsets_list = range(0,len(usersels)/10+1)
    usersels = usersels[10*offset:10*offset+10]
    template = get_template('usuario.html')
    context = ({'home': request.get_host(),
                'user': user,
                'username': request.user.username,
                'logged': logged,
                'offsets_list': offsets_list,
                'usersels': usersels})
    return HttpResponse(template.render(context))


def usuario_xml(request,user):
    xml = xmlcreate(user)
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    template = get_template('usuario_xml.html')
    context = ({'home': request.get_host(),
                'user': user,
                'username': request.user.username,
                'logged': logged,
                'xml': xml})
    return HttpResponse(template.render(context))


def about(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    template = get_template('about.html')
    context = ({'home': request.get_host(),
                'username': request.user.username,
                'logged': logged})
    return HttpResponse(template.render(context))


def loggedin(request):
    return redirect("http://" + request.get_host() + "?offset=0")


def xmlparse():
    #pagecode = urllib.urlopen("http://www.esmadrid.com/opendata/alojamientos_v1_es.xml")
    pagecode = urllib.urlopen("http://cursosweb.github.io/etc/alojamientos_es.xml")
    xmlsheet = pagecode.read()
    noticias=xmlsheet.split("<service ")
    for noticia in noticias[1:-1]:
        url = noticia.split("<web>")[1].split("</web>")[0]
        try:
            alojamiento = Alojamientos.objects.get(url=url)
            print alojamiento
        except Alojamientos.DoesNotExist:
            name = noticia.split("<name><![CDATA[")[1].split("]]></name>")[0]
            address = noticia.split("<address>")[1].split("</address>")[0]
            zipcode = noticia.split("<zipcode>")[1].split("</zipcode>")[0]
            country = noticia.split("<country>")[1].split("</country>")[0]
            latitude = noticia.split("<latitude>")[1].split("</latitude>")[0]
            longitude = noticia.split("<longitude>")[1].split("</longitude>")[0]
            city = noticia.split("<subAdministrativeArea>")[1].split("</subAdministrativeArea>")[0]
            alojamiento = Alojamientos(name=name, url=url, address=address, zipcode=zipcode, country=country, latitude=latitude, longitude=longitude, city=city)
            alojamiento.save()
            images = noticia.split('<url>')
            for image in images[1:6]:
                image_url = image.split('</url>')[0]
                image = Images(url=image_url, alojamiento=alojamiento)
                image.save()


"""def xmlparse_leng(url,usersels_orig):
    usersels = UserSels
    pagecode = urllib.urlopen(url)
    xmlsheet = pagecode.read()
    noticias=xmlsheet.split("<service ")
    for noticia in noticias[1:-1]:
        name = noticia.split("<name><![CDATA[")[1].split("]]></name>")[0]
        print name
        for usersel_orig in usersels_orig:
            print "      == " + usersel_orig.alojamiento.name
            if name == usersel_orig.alojamiento.name:
                print "Entro en el if. Vamos a parsear"
                url = noticia.split("<web>")[1].split("</web>")[0]
                address = noticia.split("<address>")[1].split("</address>")[0]
                alojamiento = Alojamientos(name=name, url=url, address=address)
                usersel = UserSels(user=usersel_orig.user, date=usersel_orig.date, alojamiento=alojamiento)
                usersels = usersels.append(usersel)
    return usersels"""


def xmlcreate(user):
    usersels = UserSels.objects.filter(user=user)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<serviceList>'
    for usersel in usersels:
        xml += '<service fechaActualizacion="' + str(datetime.datetime.now()) + '">'
        xml += "<basicData><language>es</language>"
        xml += "<name><![CDATA[" + usersel.alojamiento.name + "]]></name>"
        xml += "<email/><phone/><fax/>"
        xml += "<title><![" + usersel.alojamiento.name + "]]></title>"
        xml += "<web>" + usersel.alojamiento.url + "</web>"
        xml += "</basicdata><geoData>"
        xml += "<address>" + usersel.alojamiento.address + "</address>"
        xml += "<zipcode>" + str(usersel.alojamiento.zipcode) + "</zipcode>"
        xml += "<locality/><country>" + usersel.alojamiento.country + "</country>"
        xml += "<latitude>" + str(usersel.alojamiento.latitude) + "</latitude>"
        xml += "<longitude>" + str(usersel.alojamiento.longitude) + "</longitude>"
        xml += "<subAdministrativeArea>" + usersel.alojamiento.country + "</subAdministrativeArea>"
        xml += "</geoData><multimedia>"
        images = Images.objects.filter(alojamiento_id=usersel.alojamiento_id)
        for image in images:
            xml += '<media type="image"><description/><url>' + image.url + "</url></media>"
        xml += "</multimedia>"
        xml += "<extradata/></service>"
    xml += "</serviceList>"
    return xml
