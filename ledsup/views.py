from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
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
        messages.success(self.request, 'Orden modificado exitosamente')
        return super().form_valid(form)


# ---------------------------------- DISPOSITIVOS PAGE ----------------------------------


class ListDispositivosPage(LoginRequiredMixin, generic.ListView):
    template_name = 'ledsup/lista_dispositivos.html'
    context_object_name = 'listadoDispositivos'

    def get_queryset(self):
        return Dispositivo.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)


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
        messages.success(self.request, 'Dispositivo creado exitosamente')
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
        messages.success(self.request, 'Dispositivo editado exitosamente')
        form.instance.patch = self.request.POST['patch']

        return super().form_valid(form)


class DispositivoDelete(LoginRequiredMixin, DeleteView):
    model = Dispositivo
    success_url = reverse_lazy('ledsup:lista_dispositivos')

    def form_valid(self, form):
        messages.success(self.request, 'Dispositivo eliminado exitosamente')
        return super().form_valid(form)


# ---------------------------------- SHOWROOM PAGE ----------------------------------

def getDispositivosByIDShowroom(idShow):
    listado_de_dispositivos = list()

    show = Showroom.objects.get_queryset().filter(id=int(idShow))

    lista_num_ip = show.values('dispositivos__numero_ip')
    lista_universos = show.values('dispositivos__universo')
    lista_matriz_x = show.values('dispositivos__matriz_x')
    lista_matriz_y = show.values('dispositivos__matriz_y')
    lista_patch = show.values('dispositivos__patch')
    lista_orden = show.values('dispositivos__ordendispositivosenshowroom__orden')
    lista_tipo_led = show.values('dispositivos__tipo_led')
    lista_nombre_dispositivo = show.values('dispositivos__nombre_dispositivo')

    for num in range(len(lista_num_ip)):
        ip = lista_num_ip[num]['dispositivos__numero_ip']
        universo = lista_universos[num]['dispositivos__universo']
        matriz_x = lista_matriz_x[num]['dispositivos__matriz_x']
        matriz_y = lista_matriz_y[num]['dispositivos__matriz_y']
        patch = lista_patch[num]['dispositivos__patch']
        orden = lista_orden[num]['dispositivos__ordendispositivosenshowroom__orden']
        tipo_led = lista_tipo_led[num]['dispositivos__tipo_led']
        nombre_dispositivo = lista_nombre_dispositivo[num]['dispositivos__nombre_dispositivo']

        listado_de_dispositivos.extend([ip, universo, matriz_x, matriz_y, patch, orden, tipo_led, nombre_dispositivo])

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


class ProbarDispositivoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.POST['is_showroom_conectado']:
            messages.error(request, "Error: No se pudo establecer conexión con el servidor")

        else:
            lista = [
                request.POST['ip'], request.POST['universo'], 0, 0, 'Sin patch', '0', 'RGB'
            ]
            probar_dispositivo(self.request.user.id, lista)
            messages.info(request, f"Dispositivo {request.POST['nombre_dispositivo']} probado")

        return redirect('ledsup:lista_showroom')


class ShowroomPage(LoginRequiredMixin, generic.ListView):
    template_name = 'ledsup/showroom.html'
    context_object_name = 'listadoShowroom'

    def get_queryset(self):
        return Showroom.objects.get_queryset().filter(
            usuario__email__exact=self.request.user.email)


class ShowroomActionBase(LoginRequiredMixin, View):
    action_name = None

    def get_show_and_devices(self, request):
        show_id = int(request.POST.get('show'))
        dispositivos = getDispositivosByIDShowroom(show_id)
        return show_id, dispositivos

    def update_session(self, request, show_id, extra_data):
        data = {
            'valorShowroom': show_id,
            'active': self.action_name,
        }
        data.update(extra_data)
        request.session.update(data)


class ColorAction(ShowroomActionBase):
    action_name = 'color'

    def post(self, request, *args, **kwargs):
        show_id, dispositivos = self.get_show_and_devices(request)

        color_value = request.POST.get('color')
        velocidad = request.POST.get('velocidadColorCambioConstante')
        cambio_constante = 'checked' if request.POST.get('cambioConstanteColor') else ''

        color(self.request.user.id, dispositivos, color_value, velocidad, cambio_constante)

        self.update_session(request, show_id, {
            'col': color_value,
            'velocidadColorCambioConstante': velocidad,
            'cambioConstanteColor': cambio_constante
        })

        return redirect('ledsup:showroom')


class ScrollAction(ShowroomActionBase):
    action_name = 'scroll'

    def post(self, request, *args, **kwargs):
        show_id, dispositivos = self.get_show_and_devices(request)

        dir_scroll = request.POST.get('dirScroll')
        velocidad_scroll = request.POST.get('velocidadScroll')

        scroll(self.request.user.id, dispositivos, dir_scroll, velocidad_scroll)

        self.update_session(request, show_id, {
            'dirScroll': dir_scroll,
            'velocidadScroll': velocidad_scroll,
        })

        return redirect('ledsup:showroom')


class ScanAction(ShowroomActionBase):
    action_name = 'scan'

    def post(self, request, *args, **kwargs):
        show_id, dispositivos = self.get_show_and_devices(request)

        dir_scan = request.POST['dirScan']
        velocidad = request.POST['velocidadScan']
        color1 = request.POST['color1Scan']
        color2 = request.POST['color2Scan']

        scan(self.request.user.id, dispositivos, dir_scan, velocidad, color1, color2)

        self.update_session(request, show_id, {
            'dirScan': dir_scan,
            'velocidadScan': velocidad,
            'color1Scan': color1,
            'color2Scan': color2,
        })

        return redirect('ledsup:showroom')


class EstrellasAction(ShowroomActionBase):
    action_name = 'estrellas'

    def post(self, request, *args, **kwargs):
        show_id, dispositivos = self.get_show_and_devices(request)

        velocidad = request.POST['velocidadEstrellas']
        color1 = request.POST['color1Estrellas']
        color2 = request.POST['color2Estrellas']

        estrellas(self.request.user.id, dispositivos, velocidad, color1, color2)

        self.update_session(request, show_id, {
            'velocidadEstrellas': velocidad,
            'color1Estrellas': color1,
            'color2Estrellas': color2,
        })

        return redirect('ledsup:showroom')


#############################   Showroom CRUD  ##########################################
class ShowroomCreate(LoginRequiredMixin, CreateView):
    def get_form(self, *args, **kwargs):
        form = super(ShowroomCreate, self).get_form(*args, **kwargs)

        form.fields[
            'dispositivos'].queryset = Dispositivo.objects.get_queryset(
        ).filter(usuario__email__exact=self.request.user.email)

        form.instance.usuario = self.request.user

        return form

    model = Showroom
    success_url = reverse_lazy('ledsup:lista_showroom')
    fields = [
        'nombre_showroom',
        'dispositivos',
    ]

    def form_valid(self, form):
        messages.success(self.request, 'Showroom creado exitosamente')
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
    fields = ['dispositivos', 'nombre_showroom']

    def form_valid(self, form):
        messages.success(self.request, 'Showroom editado exitosamente')
        return super().form_valid(form)


class ShowroomDelete(LoginRequiredMixin, DeleteView):
    model = Showroom
    success_url = reverse_lazy('ledsup:lista_showroom')

    def form_valid(self, form):
        messages.success(self.request, 'Showroom eliminado exitosamente')
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
