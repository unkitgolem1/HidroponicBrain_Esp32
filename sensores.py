#modelo de sensor digital de temperatura 'ds18b20'
import machine, time, onewire, ds18x20, asyncio

class SensorTemperatura:
    def __init__(self, pin):
        self.pin_conexion_informacion = machine.Pin(pin)
        self.sensor = ds18x20.DS18X20(onewire.OneWire(self.pin_conexion_informacion))
        self.roms = self.sensor.scan()
        #Los roms son los identificadores de 64bits que tienen los sensores, gracias a esto podemos tener varios en serie... roms devuelve una lista de los dispositivos detectados
    async def leer_sensor(self):
        self.sensor.convert_temp()
        await asyncio.sleep_ms(765)
        resultados=[]
        for rom in self.roms:
            temp=self.sensor.read_temp(rom)
            resultados.append(temp)
        return resultados


class Rele:
    def __init__(self, pin):
        self.pin = pin
        self.rele = machine.Pin(pin, machine.Pin.OUT)
    def encender_rele(self):
        self.rele.value(0)
        return 'bomba_encendida'
    def apagar_rele(self):
        self.rele.value(1)
        return 'bomba_apagada'
