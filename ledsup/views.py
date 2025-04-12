import sys

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ledsup.artnet import probar_dispositivo, color, scroll, estrellas, scan
from ledsup.models import Dispositivo, Showroom, OrdenDispositivosEnShowroom
from ledsup.serializers import ShowroomSerializer, DispositivoSerializer


class OrdenDispositivosEnShowroomUpdate(LoginRequiredMixin, UpdateView):
    def get_form(self, *args, **kwargs):
        form = super(OrdenDispositivosEnShowroomUpdate,
                     self).get_form(*args, **kwargs)

        return form

    model = OrdenDispositivosEnShowroom
    success_url = reverse_lazy('ledsup:lista_showroom')
    fields = ['orden']

    def form_valid(self, form):
        messages.success(self.request, 'Orden modificado exitosamente!')
        return super().form_valid(form)


# ---------------------------------- DISPOSITIVOS PAGE ----------------------------------


class ListDispositivosPage(LoginRequiredMixin, generic.ListView):
    template_name = 'ledsup/lista_dispositivos.html'
    context_object_name = 'listadoDispositivos'

    def get_queryset(self):

        return Dispositivo.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)

    def probar_dispositivo(self):
        try:

            lista = list()
            lista.extend([self.POST['ip'], self.POST['universo'], 0, 0, 'Sin patch', '0', 'RGB'])

            probar_dispositivo(lista)

            messages.info(self, "Dispositivo " + self.POST['nombre_dispositivo'] + " probado!")

            return HttpResponseRedirect(reverse('ledsup:lista_dispositivos'))

        except:
            messages.error(self, "Error! No se pudo establecer conexion con el servidor")
            return HttpResponseRedirect(reverse('ledsup:lista_dispositivos'))


class DispositivoCreate(LoginRequiredMixin, CreateView):
    def get_form(self, *args, **kwargs):
        form = super(DispositivoCreate, self).get_form(*args, **kwargs)
        form.instance.usuario = self.request.user

        return form

    model = Dispositivo
    success_url = reverse_lazy('ledsup:lista_dispositivos')
    fields = [
        'nombre_dispositivo',
        'numero_ip',
        'universo',
        'matriz_x',
        'matriz_y',
        'tipo_led',
    ]

    def form_valid(self, form):
        messages.success(self.request, 'Dispositivo creado exitosamente!')
        form.instance.patch = self.request.POST['patch']

        return super().form_valid(form)


class DispositivoUpdate(LoginRequiredMixin, UpdateView):
    def get_form(self, *args, **kwargs):
        form = super(DispositivoUpdate, self).get_form(*args, **kwargs)
        form.instance.usuario = self.request.user

        return form

    model = Dispositivo
    success_url = reverse_lazy('ledsup:lista_dispositivos')
    fields = [
        'nombre_dispositivo',
        'numero_ip',
        'universo',
        'matriz_x',
        'matriz_y',
        'tipo_led',
    ]

    def form_valid(self, form):
        messages.success(self.request, 'Dispositivo editado exitosamente!')
        form.instance.patch = self.request.POST['patch']

        return super().form_valid(form)


class DispositivoDelete(LoginRequiredMixin, DeleteView):
    model = Dispositivo
    success_url = reverse_lazy('ledsup:lista_dispositivos')

    def form_valid(self, form):
        messages.success(self.request, 'Dispositivo eliminado exitosamente!')
        return super().form_valid(form)


# ---------------------------------- SHOWROOM PAGE ----------------------------------

def getDispositivosByIDShowroom(idShow):
    listado_de_dispositivos = list()
    # FILTRO EL SHOWROOM QUE ELIGIO EL USUARIO

    show = Showroom.objects.get_queryset().filter(id=int(idShow))

    # DE ESE SHOW TOMO IP/IPS DE LOS DISPOSITIVOS

    lista_num_ip = show.values('dispositivos__numero_ip')
    lista_universos = show.values('dispositivos__universo')
    lista_matriz_x = show.values('dispositivos__matriz_x')
    lista_matriz_y = show.values('dispositivos__matriz_y')
    lista_patch = show.values('dispositivos__patch')
    lista_orden = show.values(
        'dispositivos__ordendispositivosenshowroom__orden')
    lista_tipo_led = show.values('dispositivos__tipo_led')

    for num in range(len(lista_num_ip)):
        ip = lista_num_ip[num]['dispositivos__numero_ip']
        universo = lista_universos[num]['dispositivos__universo']
        matriz_x = lista_matriz_x[num]['dispositivos__matriz_x']
        matriz_y = lista_matriz_y[num]['dispositivos__matriz_y']
        patch = lista_patch[num]['dispositivos__patch']
        orden = lista_orden[num][
            'dispositivos__ordendispositivosenshowroom__orden']
        tipo_led = lista_tipo_led[num]['dispositivos__tipo_led']

        listado_de_dispositivos.extend(
            [ip, universo, matriz_x, matriz_y, patch, orden, tipo_led])

    return listado_de_dispositivos


class ListShowroomPage(LoginRequiredMixin, generic.ListView):
    template_name = 'ledsup/lista_showroom.html'
    context_object_name = 'listadoShowroom'

    def get_queryset(self):
        return Showroom.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordenes'] = OrdenDispositivosEnShowroom.ORDEN_DISPOSITIVOS
        context[
            'ordenesDispositivosEnShowroom'] = OrdenDispositivosEnShowroom.objects.get_queryset(
        ).filter(showroom__usuario__email__exact=self.request.user.email)

        return context


class ShowroomPage(LoginRequiredMixin, generic.ListView):
    template_name = 'ledsup/showroom.html'
    context_object_name = 'listadoShowroom'

    def get_queryset(self):

        return Showroom.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)

    def color(self):
        try:

            lista = getDispositivosByIDShowroom(self.POST['show'])

            # ARMA UN JSON Y LO ENVIA AL SERVIDOR DE PC

            color(lista, self.POST['color'])

            # DATOS PARA VOLVER A PONER LA PAGINA COMO ESTABA ##(HAY OTRA FORMA?)##

            self.session['col'] = self.POST['color']
            self.session['valorShowroom'] = int(self.POST['show'])
            self.session['active'] = 'color'
            self.session['velocidadColorCambioConstante'] = self.POST[
                'velocidadColorCambioConstante']

            if self.POST.get('cambioConstanteColor', False):
                self.session['cambioConstanteColor'] = 'checked'
            else:
                self.session['cambioConstanteColor'] = ''

            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except ConnectionRefusedError:
            messages.error(
                self, "Error! No se pudo establecer conexion con el servidor")
            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except:
            messages.error(self, "Error inesperado: ", sys.exc_info()[0])
            return HttpResponseRedirect(reverse('ledsup:showroom'))

    def scroll(self):
        try:
            lista = getDispositivosByIDShowroom(self.POST['show'])

            scroll(lista, self.POST['dirScroll'], self.POST['velocidadScroll'])

            self.session['valorShowroom'] = int(self.POST['show'])
            self.session['active'] = 'scroll'
            self.session['dirScroll'] = self.POST['dirScroll']
            self.session['velocidadScroll'] = self.POST['velocidadScroll']
            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except ConnectionRefusedError:
            messages.error(
                self, "Error! No se pudo establecer conexion con el servidor")
            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except:
            messages.error(self, "Error inesperado: ", sys.exc_info()[0])
            return HttpResponseRedirect(reverse('ledsup:showroom'))

    def scan(self):
        try:
            lista = getDispositivosByIDShowroom(self.POST['show'])

            scan(lista, self.POST['dirScan'], self.POST['velocidadScan'],
                 self.POST['color1Scan'], self.POST['color2Scan'])

            self.session['valorShowroom'] = int(self.POST['show'])
            self.session['active'] = 'scan'
            self.session['dirScan'] = self.POST['dirScan']
            self.session['velocidadScan'] = self.POST['velocidadScan']
            self.session['color1Scan'] = self.POST['color1Scan']
            self.session['color2Scan'] = self.POST['color2Scan']

            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except ConnectionRefusedError:
            messages.error(
                self, "Error! No se pudo establecer conexion con el servidor")
            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except:
            messages.error(self, "Error inesperado: ", sys.exc_info()[0])
            return HttpResponseRedirect(reverse('ledsup:showroom'))

    def estrellas(self):
        try:

            lista = getDispositivosByIDShowroom(self.POST['show'])

            estrellas(lista, self.POST['velocidadEstrellas'],
                      self.POST['color1Estrellas'],
                      self.POST['color2Estrellas'])

            self.session['valorShowroom'] = int(self.POST['show'])
            self.session['active'] = 'estrellas'

            self.session['velocidadEstrellas'] = self.POST[
                'velocidadEstrellas']
            self.session['color1Estrellas'] = self.POST['color1Estrellas']
            self.session['color2Estrellas'] = self.POST['color2Estrellas']

            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except ConnectionRefusedError:
            messages.error(
                self, "Error! No se pudo establecer conexion con el servidor")
            return HttpResponseRedirect(reverse('ledsup:showroom'))

        except:
            messages.error(self, "Error inesperado: ", sys.exc_info()[0])
            return HttpResponseRedirect(reverse('ledsup:showroom'))


class ShowroomCreate(LoginRequiredMixin, CreateView):
    def get_form(self, *args, **kwargs):
        form = super(ShowroomCreate, self).get_form(*args, **kwargs)

        form.fields[
            'dispositivos'].queryset = Dispositivo.objects.get_queryset(
        ).filter(usuario__email__exact=self.request.user.email)

        form.instance.usuario = self.request.user

        # if Dispositivo.objects.get_queryset().filter(wifi__usuario__email__exact=self.request.user.email).count() == 0:
        # form.fields['dispositivos'] = 'No existen dispositivos, agreguelos primero'
        return form

    model = Showroom
    success_url = reverse_lazy('ledsup:lista_showroom')
    fields = [
        'nombre_showroom',
        'dispositivos',
        'url_server',
    ]

    def form_valid(self, form):
        messages.success(self.request, 'Showroom creado exitosamente!')
        return super().form_valid(form)


class ShowroomUpdate(LoginRequiredMixin, UpdateView):
    def get_form(self, *args, **kwargs):
        form = super(ShowroomUpdate, self).get_form(*args, **kwargs)
        form.fields[
            'dispositivos'].queryset = Dispositivo.objects.get_queryset(
        ).filter(usuario__email__exact=self.request.user.email)

        return form

    model = Showroom
    success_url = reverse_lazy('ledsup:lista_showroom')
    fields = ['dispositivos', 'nombre_showroom', 'url_server']

    def form_valid(self, form):
        messages.success(self.request, 'Showroom editado exitosamente!')
        return super().form_valid(form)


class ShowroomDelete(LoginRequiredMixin, DeleteView):
    model = Showroom
    success_url = reverse_lazy('ledsup:lista_showroom')

    def form_valid(self, form):
        messages.success(self.request, 'Showroom eliminado exitosamente!')
        return super().form_valid(form)


# ---------------------------------- API PAGE ----------------------------------


class ShowroomViewSet(viewsets.ModelViewSet):
    serializer_class = ShowroomSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Showroom.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)


class DispositivoViewSet(viewsets.ModelViewSet):
    serializer_class = DispositivoSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Dispositivo.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)
