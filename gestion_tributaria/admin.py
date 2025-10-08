from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Perfil, CalificacionTributaria, CargaMasiva, LogOperacion


# ============================================
# INLINE: PERFIL EN USUARIO
# ============================================
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil'
    fields = ('rol', 'nombre_completo', 'rut')


# ============================================
# EXTENDER ADMIN DE USUARIO
# ============================================
class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'get_rol', 'get_nombre_completo', 'is_active', 'date_joined')
    list_filter = ('is_active',)
    
    def get_rol(self, obj):
        return obj.perfil.get_rol_display() if hasattr(obj, 'perfil') else '-'
    get_rol.short_description = 'Rol'
    
    def get_nombre_completo(self, obj):
        return obj.perfil.nombre_completo if hasattr(obj, 'perfil') else '-'
    get_nombre_completo.short_description = 'Nombre Completo'


# Re-registrar User con el nuevo admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ============================================
# ADMIN: CALIFICACIÓN TRIBUTARIA
# ============================================
@admin.register(CalificacionTributaria)
class CalificacionTributariaAdmin(admin.ModelAdmin):
    list_display = (
        'instrumento', 
        'ejercicio', 
        'mercado', 
        'fecha_pago', 
        'secuencia_evento',
        'get_usuario',
        'origen',
        'es_local',
        'updated_at'
    )
    list_filter = (
        'ejercicio', 
        'mercado', 
        'origen', 
        'es_local',
        'tipo_sociedad',
        'acogido_isfut'
    )
    search_fields = (
        'instrumento', 
        'descripcion',
        'usuario__username',
    )
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'usuario',
                'carga_masiva',
                ('ejercicio', 'mercado'),
                'instrumento',
                ('fecha_pago', 'secuencia_evento'),
                ('numero_dividendo', 'tipo_sociedad'),
                'acogido_isfut',
                'descripcion',
            )
        }),
        ('Valores Base', {
            'fields': (
                'valor_historico',
                'factor_actualizacion',
            )
        }),
        ('Factores Tributarios (8-19)', {
            'fields': (
                ('factor_8', 'factor_9', 'factor_10'),
                ('factor_11', 'factor_12', 'factor_13'),
                ('factor_14', 'factor_15', 'factor_16'),
                ('factor_17', 'factor_18', 'factor_19'),
            ),
            'classes': ('collapse',),
        }),
        ('Factores Tributarios (20-31)', {
            'fields': (
                ('factor_20', 'factor_21', 'factor_22'),
                ('factor_23', 'factor_24', 'factor_25'),
                ('factor_26', 'factor_27', 'factor_28'),
                ('factor_29', 'factor_30', 'factor_31'),
            ),
            'classes': ('collapse',),
        }),
        ('Factores Tributarios (32-37)', {
            'fields': (
                ('factor_32', 'factor_33', 'factor_34'),
                ('factor_35', 'factor_36', 'factor_37'),
            ),
            'classes': ('collapse',),
        }),
        ('Metadatos', {
            'fields': (
                ('origen', 'es_local'),
                ('created_at', 'updated_at'),
            )
        }),
    )
    
    def get_usuario(self, obj):
        return obj.usuario.perfil.nombre_completo if hasattr(obj.usuario, 'perfil') else obj.usuario.username
    get_usuario.short_description = 'Corredor'
    
    def get_queryset(self, request):
        """Administradores ven todo, corredores solo lo suyo"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'perfil') and request.user.perfil.rol == 'ADMIN':
            return qs
        return qs.filter(usuario=request.user)


# ============================================
# ADMIN: CARGA MASIVA
# ============================================
@admin.register(CargaMasiva)
class CargaMasivaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_archivo',
        'tipo_carga',
        'get_usuario',
        'registros_procesados',
        'registros_exitosos',
        'registros_fallidos',
        'fecha_carga'
    )
    list_filter = ('tipo_carga', 'fecha_carga')
    search_fields = ('nombre_archivo', 'usuario__username')
    readonly_fields = ('fecha_carga',)
    
    def get_usuario(self, obj):
        return obj.usuario.perfil.nombre_completo if hasattr(obj.usuario, 'perfil') else obj.usuario.username
    get_usuario.short_description = 'Usuario'


# ============================================
# ADMIN: LOG DE OPERACIONES
# ============================================
@admin.register(LogOperacion)
class LogOperacionAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_hora',
        'get_usuario',
        'operacion',
        'get_calificacion',
        'ip_address'
    )
    list_filter = ('operacion', 'fecha_hora')
    search_fields = ('usuario__username', 'calificacion__instrumento')
    readonly_fields = (
        'usuario', 'calificacion', 'carga_masiva', 'operacion',
        'datos_anteriores', 'datos_nuevos', 'ip_address', 'fecha_hora'
    )
    
    def get_usuario(self, obj):
        return obj.usuario.perfil.nombre_completo if hasattr(obj.usuario, 'perfil') else obj.usuario.username
    get_usuario.short_description = 'Usuario'
    
    def get_calificacion(self, obj):
        return str(obj.calificacion) if obj.calificacion else '-'
    get_calificacion.short_description = 'Calificación'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


# ============================================
# PERSONALIZACIÓN DEL SITIO ADMIN
# ============================================
admin.site.site_header = 'Sistema de Calificaciones Tributarias NUAM'
admin.site.site_title = 'Admin NUAM'
admin.site.index_title = 'Panel de Administración'