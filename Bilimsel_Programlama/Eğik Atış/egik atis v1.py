# -*- coding: utf-8 -*-
"""
Eğik atış örneği v1.

Basit bir vektör nesnesi ile çalışma.
"""
# sonradan gerekecek kütüphanelerini çağır
import matplotlib.pyplot as plt
import math

# Kütleçekimi Sabiti [m/s^2]
gDünya = 9.81


class zamanKonumHız:
   'Zaman, 2D konum ve 2D hız değerlerini içeren vektör sınıfı'
   t = 0
   rx, ry = 0, 0
   vx, vy = 0, 0

   def __init__(self, t0, rx0, ry0, vx0, vy0):
      self.t  = t0
      self.rx = rx0
      self.ry = ry0
      self.vx = vx0
      self.vy = vy0

def tAnındaZamanKonumHız(t, pvt0, g=gDünya):
    """Verilen bir t zamanı için yeni konum ve hızı döndürür"""
    tYeni  = pvt0.t + t
    rxYeni = pvt0.rx + pvt0.vx * t
    ryYeni = pvt0.ry + pvt0.vy * t + (-1/2 * g * t**2)
    vxYeni = pvt0.vx 
    vyYeni = pvt0.vy + (-g) * t
    return zamanKonumHız(tYeni, rxYeni, ryYeni, vxYeni, vyYeni)

# başlangıç zamanı
t0 = 0
# bitiş zamanı (sn)
tSon = 100
# adım büyüklüğü (sn)
tAdım = 0.5

# başlangıç hızı (m/sn) ve atış açısı (derece)
v0 = 100 
yükselmeAçısı = 50 

# başlangıç konum ve hız
pvt0 = zamanKonumHız(t0, 0, 0, v0*math.cos(math.radians(yükselmeAçısı)), v0*math.sin(math.radians(yükselmeAçısı)))

# Zaman, yükseklik ve hız bilgilerini içeren vektör listelerini oluştur
pvtList = []

t = pvt0.t
h = pvt0.ry 
while t<=tSon and h>=0:
    pvtList.append( tAnındaZamanKonumHız(t, pvt0) )
    h = pvtList[-1].ry
    t += tAdım

# konum grafiği 
plt.plot( [pvt.rx for pvt in pvtList], [pvt.ry for pvt in pvtList])

plt.title("Konum")
plt.xlabel("x konum (m)")
plt.ylabel('y konum (m)')

plt.show()

# hız grafiği
plt.plot( [pvt.vx for pvt in pvtList], [pvt.vy for pvt in pvtList])

plt.title("Hız")
plt.xlabel("x hız (m/sn)")
plt.ylabel('y hız (m/sn)')

plt.show()