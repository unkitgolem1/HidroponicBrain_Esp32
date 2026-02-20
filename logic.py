from sensores import Rele, SensorTemperatura
from models import EstadoSistema, ParametrosSistema
import asyncio, gc, ujson, urequests



async def logica_riego(rele, contexto):
    while True:
        '''
        Prender la bomba si o si siempre es logica de negocio , unegociable siempre,
        se prende 15 min se apaga 20, si en esos 20 la temperatura empieza asubir dios mio hay candela entonces chicoleamos
        '''
        rele.enceder_rele()
        contexto.estado_actual = EstadoSistema.ACTIVO
        await asyncio.sleep(900)
        rele.apagar_rele()
        contexto.estado_actual = EstadoSistema.REPOSO
        contexto.estado_forzado = False
        temporizador = 0
        while temporizador < 1200:
            await asyncio.sleep(1)
            temporizador +=
            if contexto.temperatura >= 30:
                break
        await asyncio.sleep(5)
        
        # Anunciar al usuario ,si no se apaga la bomba es porque detecta que la temperatura dle agua es alta ...
        
# Aqui pronto estara la logica de abonado

async def comunicaciones(contexto):
    URL = 'http://192.0.0.10:3214/sistema'
    while True:
        res = None #para evitar errores por si no llega la peticion
        try:
            playload = {
                "Temperatura": contexto.temperatura,
                "Estado_actual": contexto.estado_actual
                }
            res = urequests(URL, json=playload, timeout = 3)
            if res.status_code == 200:
                ordenes = res.json()
                contexto.estado_forzado = ordenes.get("Bomba_manual" , False)
        except Exception as e:
            print(f'Error de red{e}')
        finally:
            if res:
                res.close()
            gc.collect()
        
        await asyncio.sleep(10)