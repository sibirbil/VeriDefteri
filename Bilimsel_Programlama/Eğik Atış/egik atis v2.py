# -*- coding: utf-8 -*-
"""
Eğik atış örneği v2.

Euler sayısal entegrasyon.
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

      
   def konumBüyüklüğü(self):
       """Konum vektörünün büyüklüğünü döndürür"""
       return math.sqrt(self.rx*self.rx+self.ry*self.ry)

   def hızBüyüklüğü(self):
       """Hız vektörünün büyüklüğünü döndürür"""
       return math.sqrt(self.vx*self.vx+self.vy*self.vy)


def tAnındaZamanKonumHız(t, pvt0, g=gDünya):
    """Verilen bir t zamanı için yeni konum ve hızı döndürür"""
    tYeni  = pvt0.t + t
    rxYeni = pvt0.rx + pvt0.vx * t
    ryYeni = pvt0.ry + pvt0.vy * t + (-1/2 * g * t**2)
    vxYeni = pvt0.vx 
    vyYeni = pvt0.vy + (-g) * t
    return zamanKonumHız(tYeni, rxYeni, ryYeni, vxYeni, vyYeni)

def eulerZamanKonumHız(dt, pvt, g=gDünya):
    """Verilen bir dt adım büyüklüğü için yeni konum ve hızı döndürür"""
    tYeni  = pvt.t  + dt
    rxYeni = pvt.rx + pvt.vx * dt
    ryYeni = pvt.ry + pvt.vy * dt 
    vxYeni = pvt.vx + 0 * dt
    vyYeni = pvt.vy + (-g) * dt
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

# ilk değerleri doldur
gerçekPvtList = [pvt0]
numPvtList    = [pvt0]
hataPvtList   = [zamanKonumHız(t0, 0, 0, 0, 0)]

# Döngüyü çalıştır
t = gerçekPvtList[0].t + tAdım
h = gerçekPvtList[0].ry 
while t<=tSon and h>=0:
    pvtGerçek = tAnındaZamanKonumHız(t, pvt0)
    gerçekPvtList.append( pvtGerçek )
    
    pvtNum = eulerZamanKonumHız(tAdım, numPvtList[-1])
    numPvtList.append( pvtNum )
    
    hataPvt = zamanKonumHız(t, pvtNum.rx-pvtGerçek.rx, pvtNum.ry-pvtGerçek.ry, pvtNum.vx-pvtGerçek.vx, pvtNum.vy-pvtGerçek.vy)
    hataPvtList.append(hataPvt)
    
    h = gerçekPvtList[-1].ry
    t += tAdım



# konum grafiği 
plt.plot( [pvt.rx for pvt in gerçekPvtList], [pvt.ry for pvt in gerçekPvtList], label="gerçek")
plt.plot( [pvt.rx for pvt in numPvtList], [pvt.ry for pvt in numPvtList], label="Euler (" + str(tAdım) + " s)")

plt.title(r"Konum")
plt.xlabel("x konum (m)")
plt.ylabel('y konum (m)')
plt.legend(loc=3)

plt.show()

# hiz grafiği
plt.plot( [pvt.vx for pvt in gerçekPvtList], [pvt.vy for pvt in gerçekPvtList], label="gerçek")
plt.plot( [pvt.vx for pvt in numPvtList], [pvt.vy for pvt in numPvtList], label="Euler (" + str(tAdım) + " s)")

plt.title(r"Hız")
plt.xlabel("x hız (m/s)")
plt.ylabel('y hız (m/s)')
plt.legend(loc=3)

plt.show()

# hata grafikleri 
plt.subplot(211)
plt.plot( [pvt.t for pvt in hataPvtList], [pvt.konumBüyüklüğü() for pvt in hataPvtList])

plt.title(r"Konum ve Hız Hatası Değişimi (" + str(tAdım) + " s)")
plt.xlabel("zaman (s)")
plt.ylabel('konum hatası (m)')

plt.subplot(212)
plt.plot( [pvt.t for pvt in hataPvtList], [pvt.hızBüyüklüğü() for pvt in hataPvtList])

# plt.title(r"Hız Değişimi ($ v = gt $)")
plt.xlabel("zaman (s)")
plt.ylabel('hız hatası (m/s)')

plt.show()