import asyncio
from models import EstadoSistema, Parametro
from logic import logica_riego, comunicaciones
from sensores import Rele, SensorTemperatura

#funciones
async def sensor_live(sensor , estado):
# De querer agragar mas sensores para que esten en vivo agregar en esta funcion
    while True:
        try:
            nueva_lectura = await sensor.leer_sensor()
            if nueva_lectura is not None:
                estado.temperatura = nueva_lectura[0] #ojo aqui, leer_sensor devuelve lista, chacar la clase del sensor
            else:
                print('Advertencia, el sensor no esta dando se;al')
        except Exception as e:
            print(f'Error grave en la lectura: {e}')
        await asyncio.sleep(2)

async def main():
# configurar infraestructura
    temp = SensorTemperatura(12)
    bomba = Rele(4)
# Instanciar EstadoSistema
    contexto = ParametrosSistema()

    await asyncio.gather(
    sensor_live(temp, contexto),
    logica_riego(bomba, contexto),
    comunicaciones(contexto)
    )

if __name__ == '__main__':
    asyncio.run(main())
    asyncio.new_event_loop()
