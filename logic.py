from sensores import Rele, SensorTemperatura
from models import EstadoSistema, ParametrosSistema
from umqtt.simple import MQTTClient
import asyncio, gc, ujson, time



async def logica_riego(rele, contexto):
    while True:
        # --- MODO MANUAL (FORZADO) ---
        if contexto.estado_forzado:
            rele.encender_rele()
            contexto.estado_actual = EstadoSistema.ACTIVO
            # Mantenemos la bomba encendida mientras esté forzada manualmente
            while contexto.estado_forzado:
                await asyncio.sleep(1)
            # Cuando el usuario la apaga desde el remoto, reiniciamos el ciclo automático
            continue

        # --- MODO AUTOMÁTICO ---
        '''
        Prender la bomba si o si siempre es logica de negocio , unegociable siempre,
        se prende 15 min se apaga 20, si en esos 20 la temperatura empieza asubir dios mio hay candela entonces chicoleamos
        '''
        rele.encender_rele()
        contexto.estado_actual = EstadoSistema.ACTIVO
        
        # 15 minutos encendida (interrumpible si el usuario activa el modo manual)
        temporizador_on = 0
        while temporizador_on < 900 and not contexto.estado_forzado:
            await asyncio.sleep(1)
            temporizador_on += 1
            
        # Si nos forzaron el encendido manual a la mitad del ciclo, reiniciamos el loop
        if contexto.estado_forzado:
            continue

        rele.apagar_rele()
        contexto.estado_actual = EstadoSistema.REPOSO
        
        # 20 minutos apagada (interrumpible por orden manual o si sube mucho la temperatura)
        temporizador_off = 0
        while temporizador_off < 1200 and not contexto.estado_forzado:
            await asyncio.sleep(1)
            temporizador_off += 1
            if contexto.temperatura >= 29: # 29°C según tu README
                break
                
        await asyncio.sleep(1) # Pequeña pausa de seguridad antes de reiniciar el while True
        
        # Anunciar al usuario ,si no se apaga la bomba es porque detecta que la temperatura dle agua es alta ...
        
# Aqui pronto estara la logica de abonado

async def comunicaciones(contexto):
    MQTT_BROKER = '192.0.0.10'
    CLIENT_ID = 'ESP32_Control_Sistema'
    TOPIC_ESTADO = b'esp32/estado'
    TOPIC_ORDENES = b'esp32/ordenes'

    def sub_cb(topic, msg):
        if topic == TOPIC_ORDENES:
            try:
                ordenes = ujson.loads(msg.decode('utf-8'))
                if 'Bomba_manual' in ordenes:
                    contexto.estado_forzado = ordenes['Bomba_manual']
            except Exception as e:
                print(f'Error decodificando ordenes: {e}')

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(sub_cb)
    # Bucle para conectar al server
    conectado = False
    while not conectado:
        try:
            client.connect()
            client.subscribe(TOPIC_ORDENES)
            conectado = True
        except Exception as e:
            await asyncio.sleep(5)

    while True:
        try:
            client.check_msg()
            playload = {
                "Temperatura": contexto.temperatura,
                "date": time.time(),
                "Estado_actual": contexto.estado_actual
            }
            playload_str = ujson.dumps(playload)
            client.publish(TOPIC_ESTADO, playload_str.encode('utf-8'))
        except Exception as e:
            print(f'Error de red: {e}')
            conectado = False
            while not conectado:
                try:
                    client.connect()
                    client.subscribe(TOPIC_ORDENES)
                    conectado = True
                except:
                    await asyncio.sleep(5)
        finally:
            gc.collect()
        await asyncio.sleep(10)
