from micropython import const
class EstadoSistema:
    REPOSO = const(0)
    ACTIVO = const(1)
    ALERTA = const(2)

class ParametrosSistema:
    def __init__ (self):
        self.bombas_activa = False
        self.temperatura = 0.0
        self.estado_actual = EstadoSistema.REPOSO
        self.estado_forzado = False

