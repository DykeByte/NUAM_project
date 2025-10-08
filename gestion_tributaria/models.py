from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# ============================================
# MODELO: PERFIL DE USUARIO
# ============================================
class Perfil(models.Model):
    ROL_CHOICES = [
        ('CORREDOR', 'Corredor'),
        ('ADMIN', 'Administrador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='CORREDOR')
    nombre_completo = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        db_table = 'perfil'
    
    def __str__(self):
        return f"{self.nombre_completo} ({self.get_rol_display()})"


# ============================================
# MODELO: CARGA MASIVA
# ============================================
class CargaMasiva(models.Model):
    TIPO_CHOICES = [
        ('FACTORES', 'Factores Calculados'),
        ('MONTOS', 'Montos DJ1948'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cargas_masivas')
    tipo_carga = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nombre_archivo = models.CharField(max_length=255)
    registros_procesados = models.IntegerField(default=0)
    registros_exitosos = models.IntegerField(default=0)
    registros_fallidos = models.IntegerField(default=0)
    errores_detalle = models.TextField(blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Carga Masiva'
        verbose_name_plural = 'Cargas Masivas'
        db_table = 'carga_masiva'
        ordering = ['-fecha_carga']
    
    def __str__(self):
        return f"Carga {self.tipo_carga} - {self.nombre_archivo} ({self.fecha_carga.strftime('%d/%m/%Y')})"


# ============================================
# MODELO: CALIFICACIÓN TRIBUTARIA
# ============================================
class CalificacionTributaria(models.Model):
    MERCADO_CHOICES = [
        ('ACN', 'Acciones'),
        ('CFI', 'Renta Fija'),
        ('FM', 'Fondos Mutuos'),
    ]
    
    TIPO_SOCIEDAD_CHOICES = [
        ('A', 'Abierta'),
        ('C', 'Cerrada'),
    ]
    
    ORIGEN_CHOICES = [
        ('MANUAL', 'Ingreso Manual'),
        ('MASIVO', 'Carga Masiva'),
        ('SISTEMA', 'Sistema Bolsa'),
    ]
    
    # Relaciones
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='calificaciones',
        help_text='Corredor dueño de la calificación'
    )
    carga_masiva = models.ForeignKey(
        CargaMasiva, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='calificaciones'
    )
    
    # Datos básicos
    ejercicio = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        help_text='Año comercial'
    )
    mercado = models.CharField(max_length=3, choices=MERCADO_CHOICES)
    instrumento = models.CharField(max_length=50, help_text='Nombre o código del instrumento')
    fecha_pago = models.DateField(help_text='Fecha de pago del dividendo')
    secuencia_evento = models.IntegerField(help_text='Secuencia superior a 10.000')
    numero_dividendo = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    tipo_sociedad = models.CharField(max_length=1, choices=TIPO_SOCIEDAD_CHOICES)
    acogido_isfut = models.BooleanField(default=False, help_text='Acogido a ISFUT/ISIFT')
    
    # Valores base
    valor_historico = models.DecimalField(
        max_digits=18, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    factor_actualizacion = models.DecimalField(
        max_digits=9, 
        decimal_places=8, 
        default=Decimal('0.00000000')
    )
    
    # Factores tributarios (8-19)
    factor_8 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Con crédito IDPC >= 01.01.2017'
    )
    factor_9 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Con crédito IDPC <= 31.12.2016'
    )
    factor_10 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Con derecho a crédito IDPC voluntario'
    )
    factor_11 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Sin derecho a crédito'
    )
    factor_12 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Rentas RAP y Diferencia Inicial'
    )
    factor_13 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    factor_14 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    factor_15 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    factor_16 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    factor_17 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    factor_18 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    factor_19 = models.DecimalField(
        max_digits=9, decimal_places=8, default=Decimal('0.00000000'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    
    # Factores 20-37 (mismo patrón)
    factor_20 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_21 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_22 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_23 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_24 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_25 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_26 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_27 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_28 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_29 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_30 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_31 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_32 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_33 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_34 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_35 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_36 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    factor_37 = models.DecimalField(max_digits=9, decimal_places=8, default=Decimal('0.00000000'), validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Metadatos
    origen = models.CharField(max_length=10, choices=ORIGEN_CHOICES, default='MANUAL')
    es_local = models.BooleanField(
        default=True, 
        help_text='True: local del corredor | False: compartido del sistema'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Calificación Tributaria'
        verbose_name_plural = 'Calificaciones Tributarias'
        db_table = 'calificacion_tributaria'
        ordering = ['-ejercicio', '-fecha_pago']
        indexes = [
            models.Index(fields=['usuario', 'ejercicio', 'mercado']),
            models.Index(fields=['instrumento', 'fecha_pago']),
        ]
    
    def __str__(self):
        return f"{self.instrumento} - {self.ejercicio} - Sec.{self.secuencia_evento}"
    
    def clean(self):
        """Validación: Suma factores 8-16 <= 1"""
        from django.core.exceptions import ValidationError
        suma = sum([
            self.factor_8, self.factor_9, self.factor_10, self.factor_11,
            self.factor_12, self.factor_13, self.factor_14, self.factor_15, self.factor_16
        ])
        if suma > 1:
            raise ValidationError(
                f'La suma de los factores 8 al 16 no puede superar 1. Suma actual: {suma}'
            )


# ============================================
# MODELO: LOG DE OPERACIONES
# ============================================
class LogOperacion(models.Model):
    OPERACION_CHOICES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('CARGA', 'Carga Masiva'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    calificacion = models.ForeignKey(
        CalificacionTributaria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='logs'
    )
    carga_masiva = models.ForeignKey(
        CargaMasiva,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs'
    )
    
    operacion = models.CharField(max_length=10, choices=OPERACION_CHOICES)
    datos_anteriores = models.JSONField(null=True, blank=True, help_text='Estado antes de la operación')
    datos_nuevos = models.JSONField(null=True, blank=True, help_text='Estado después de la operación')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Operación'
        verbose_name_plural = 'Logs de Operaciones'
        db_table = 'log_operacion'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.get_operacion_display()} - {self.usuario.username} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"