from djongo import models

class TipoDNI(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nro_dni = models.IntegerField()
    tipo_dni = models.ForeignKey(TipoDNI, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class MedioDePago(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Entrada(models.Model):
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Venta(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleDeVenta(models.Model):
    descripcion = models.CharField(max_length=100)
    cant_entradas = models.IntegerField()
    importe_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
