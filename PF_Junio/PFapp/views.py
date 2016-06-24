from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import urllib, datetime
from models import Alojamientos
from models import Images
from models import Comments
from models import UserSels
from models import Titles
from models import Prefs

# Create your views here
def prueba(request):
    context={}
    return render(request,'prueba.html',context)

def main(request):
    dic = {}
    idlist = []
    comments = []
    if request.user.is_authenticated:
        xmlparse()
    offset = int(request.GET['offset'])
    # Creo un diccionario con el numero de comentarios asociados a cada alojamiento
    for alojamiento in Alojamientos.objects.all():
        dic[alojamiento.id] = len(Comments.objects.filter(alojamiento_id=alojamiento.id))
    # Bucle decreciente desde el numero de usuarios para encontrar los alojamientos con mas comentarios
    for n in range(1,len(User.objects.all()))[::-1]:
        for i in dic.keys():
            if dic[i] == n:
                idlist.append(i)
                if len(idlist) == 10:
                    break
    # Extraigo los ids q acabo de guardar
    for i in idlist:
        for comment in Comments.objects.all():
            if comment.alojamiento_id==i:
                comments.append(comment)
    context = ({'home': request.get_host(),
                'request': request,
                'usuarios': User.objects.all(),
                'offset': offset,
                'offsets_list': range(0,len(comments)/10+1),
                'comments': comments[offset*10:offset*10+10]})
    return render(request,'main.html',context)

@csrf_exempt
def alojamientos(request):
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
    context = ({'home': request.get_host(),
                'request': request,
                'filt': filt,
                'offset': offset,
                'offsets_list': offsets_list,
                'alojamientos': alojamientos})
    return render(request,'alojamientos.html',context)


@csrf_exempt
def alojamiento(request,ident):
    if request.user.is_authenticated:
        try:
            usersel = UserSels.objects.get(user=request.user.username, alojamiento_id=ident)
        except UserSels.DoesNotExist:
            usersel = UserSels(user=request.user.username, date=datetime.datetime.now(), alojamiento_id=ident)
            usersel.save()
    if request.method == 'POST':
        comment = Comments(user=request.user.username, text=request.POST['comment'], date=datetime.datetime.now(), alojamiento_id=ident)
        comment.save()
    try:
        comment = Comments.objects.get(user=request.user.username, alojamiento_id=ident)
        can_comment = False
    except Comments.DoesNotExist:
        can_comment = True
    context = ({'home': request.get_host(),
                'request': request,
                'alojamiento': Alojamientos.objects.get(id=ident),
                'images': Images.objects.filter(alojamiento_id=ident),
                'can_comment': can_comment})
    return render(request,'alojamiento.html',context)


@csrf_exempt
def usuario(request,user):
    usersels = UserSels.objects.filter(user=user)
    if request.method == 'POST':
        try:
            title = request.POST['title']
            newtitle = Titles(user=user, title=title)
            try:
                Titles.objects.get(user=user).delete()
                newtitle.save()
            except:
                newtitle.save()
        except KeyError:
            try:
                size = request.POST['size']
                try:
                    prefs = Prefs.objects.get(user=user)
                    prefs = Prefs(user=user, size=size, bgcolor=prefs.bgcolor)
                    Prefs.objects.get(user=user).delete()
                    prefs.save()
                except Prefs.DoesNotExist:
                    prefs = Prefs(user=user, size=size, bgcolor='black')
                    prefs.save()
                prefs.save
            except KeyError:
                try:
                    bgcolor = request.POST['bgcolor']
                    try:
                        prefs = Prefs.objects.get(user=user)
                        prefs = Prefs(user=user, size=prefs.size, bgcolor=bgcolor)
                        Prefs.objects.get(user=user).delete()
                        prefs.save()
                    except Prefs.DoesNotExist:
                        prefs = Prefs(user=user, size=2, bgcolor=bgcolor)
                        prefs.save()
                except:
                    if request.POST['leng'] == 'Ingles':
                        #xmlparse_leng("http://www.esmadrid.com/opendata/alojamientos_v1_en.xml")
                        usersels = xmlparse_leng("http://cursosweb.github.io/etc/alojamientos_en.xml",usersels)
                    elif request.POST['leng'] == 'Frances':
                        #xmlparse_leng("http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml")
                        usersels = xmlparse_leng("http://cursosweb.github.io/etc/alojamientos_fr.xml",usersels)
    try:
        title = Titles.objects.get(user=user)
        title = title.title
    except Titles.DoesNotExist:
        title = "Pagina del usuario " + user
    try:
        prefs = Prefs.objects.get(user=user)
        has_prefs = True
    except Prefs.DoesNotExist:
        prefs = None
        has_prefs = False
    offset = int(request.GET['offset'])
    context = ({'home': request.get_host(),
                'request': request,
                'userpage': user,
                'offset': offset,
                'title':title,
                'has_prefs': has_prefs,
                'prefs': prefs,
                'offsets_list': range(0,len(usersels)/10+1),
                'usersels': usersels[10*offset:10*offset+10]})
    return render(request,'usuario.html',context)


def usuario_xml(request,user):
    context = ({'home': request.get_host(),
                'request': request,
                'userpage': user,
                'xml': xmlcreate(user)})
    return render(request,'usuario_xml.html',context)


def about(request):
    context = ({'home': request.get_host(),
                'request': request})
    return render(request,'about.html',context)


def loggedin(request):
    return redirect("http://" + request.get_host() + "?offset=0")


def xmlparse():
    #pagecode = urllib.urlopen("http://www.esmadrid.com/opendata/alojamientos_v1_es.xml")
    pagecode = urllib.urlopen("http://cursosweb.github.io/etc/alojamientos_es.xml")
    xmlsheet = pagecode.read()
    noticias = xmlsheet.split("<service ")
    for noticia in noticias[1:-1]:
        url = noticia.split("<web>")[1].split("</web>")[0]
        try:
            alojamiento = Alojamientos.objects.get(url=url)
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


def xmlparse_leng(url,usersels_orig):
    usersels = []
    pagecode = urllib.urlopen(url)
    xmlsheet = pagecode.read()
    noticias = xmlsheet.split("<service ")
    for noticia in noticias[1:-1]:
        name = noticia.split("<name><![CDATA[")[1].split("]]></name>")[0]
        for usersel_orig in usersels_orig:
            if name == usersel_orig.alojamiento.name:
                url = noticia.split("<web>")[1].split("</web>")[0]
                address = noticia.split("<address>")[1].split("</address>")[0]
                alojamiento = Alojamientos(name=name, url=url, address=address)
                usersel = UserSels(user=usersel_orig.user, date=usersel_orig.date, alojamiento=alojamiento)
                usersels.append(usersel)
                # Como puedo hacer esto?
    return usersels


def xmlcreate(user):
    usersels = UserSels.objects.filter(user=user)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<serviceList>'
    for usersel in usersels:
        xml += '<service fechaActualizacion="' + str(datetime.datetime.now()) + '">'
        xml += "<basicData>"
        xml += "<language>es</language>"
        xml += "<name><![CDATA[" + usersel.alojamiento.name + "]]></name>"
        xml += "<email/><phone/><fax/>"
        xml += "<title><![" + usersel.alojamiento.name + "]]></title>"
        xml += "<web>" + usersel.alojamiento.url + "</web>"
        xml += "</basicData>"
        xml += "<geoData>"
        xml += "<address>" + usersel.alojamiento.address + "</address>"
        xml += "<zipcode>" + str(usersel.alojamiento.zipcode) + "</zipcode>"
        xml += "<locality/><country>" + usersel.alojamiento.country + "</country>"
        xml += "<latitude>" + str(usersel.alojamiento.latitude) + "</latitude>"
        xml += "<longitude>" + str(usersel.alojamiento.longitude) + "</longitude>"
        xml += "<subAdministrativeArea>" + usersel.alojamiento.country + "</subAdministrativeArea>"
        xml += "</geoData>"
        xml += "<multimedia>"
        images = Images.objects.filter(alojamiento_id=usersel.alojamiento_id)
        for image in images:
            xml += '<media type="image"><description/><url>' + image.url + "</url></media>"
        xml += "</multimedia>"
        xml += "<extradata/></service>"
    xml += "</serviceList>"
    return xml

# PENDIENTE:
#   - Colocar el formulario de login/out a la derecha del banner
#   - Si me sobra tiempo puedo hacer lo de dar puntuaciones a los alojamientos

# HECHO:
#   - Hacer login/out con un formulario - OK
#   - Formulario para cambiar el .css para un usuario determinado - OK
#   - Hacer bien el xml - OK
#   - Mostrar tmb una imagen de los hoteles en pequenyo formato - OK
#   - En /usuario, pedir la pagina en otro idioma (solo si el usuario esta autenticado y en su pagina) - OK
#   - En main, mostrar los 10 alojamientos con mas comentarios . OK
#   - Poner titulo a las paginas de los usuarios (solo si el usuario esta autenticado y en su pagina) - OK
#   - Solo un comentario por usuario y alojamiento - OK
#   - Definir color y tamanyo de la letra y el color de fondo en el/los .css - OK
#   - Cargar los datos solo cuando un usuario lo pida (para mi va a ser cuando un usuario autenticado acceda a la pagina principal) - OK
