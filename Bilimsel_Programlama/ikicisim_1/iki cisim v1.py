# -*- coding: utf-8 -*-
"""
İki cisim problemi örneği v1.

Numpy ve adım büyüklüğü analizi.

Hazırlayan: Egemen Imre, 2018
"""
# sonradan gerekecek kütüphaneleri çağır
import matplotlib.pyplot as plt
import numpy as np


# Kütleçekimi Sabiti [m^3/s^2]
muDünya = 398600.5*1E9


class ZamanKonumHız:
   """
    Zaman, 2D konum ve 2D hız değerlerini içeren vektör sınıfı
   """
   t = 0
   r = np.zeros(2)
   v = np.zeros(2)

   def __init__(self, t0, rx0, ry0, vx0, vy0):
       """
       Zaman, konum ve hızı ilk değerleriyle başlatır.
       
       Arguments:
           t0  {float} -- zaman (s)
           rx0 {float} -- x ekseninde konum (m)
           ry0 {float} -- y ekseninde konum (m)
           vx0 {float} -- x ekseninde hız (m/s)
           vy0 {float} -- y ekseninde hız (m/s)
      """
       self.t = t0      
       self.r = np.array([rx0, ry0])
       self.v = np.array([vx0, vy0])

      
   def konumBüyüklüğü(self):
       """Konum vektörünün büyüklüğünü döndürür
               
        Returns:
           float -- Konum vektörünün büyüklüğü ($m$)
       """
       return np.linalg.norm(self.r)

   def hızBüyüklüğü(self):
       """Hız vektörünün büyüklüğünü döndürür
        
        Returns:
           float -- Hız vektörünün büyüklüğü ($m^2/s^2$)
        """
       return np.linalg.norm(self.v)

   def spesifikEnerji(self):
       """
       Spesifik enerjiyi hesaplar.

       Spesifik enerji birim kütleye düşen enerji olarak tanımlanır

       $e =  \frac{1}{2} v^2 - \frac{\mu}{r} $
       
       Returns:
           float -- spesifik enerji ($m^2/s^2$)
       """
       return 0.5*self.v.dot(self.v) - muDünya/self.konumBüyüklüğü()

   def ivme (self, mu=muDünya):
       """
       İvmeyi hesaplar
       
       İki cisim problemine göre bu konum ve hıza ait ivmeyi hesaplar.
       
       Keyword Arguments:
           mu {float} -- Kütleçekimi Sabiti (m^3/s^2) (default: {muDünya})
       
       Returns:
           {ndarray} -- İvme vektörü ($m/s^2$)
       """
       return -mu/np.power(self.konumBüyüklüğü(), 3) * self.r


# *********** fonksiyon tanımları ***********

def eulerZamanKonumHız(dt, pvt, mu=muDünya):
    """
    Verilen bir dt adım büyüklüğü kadar zaman konum ve hızı Euler Metodu ile ilerletir.
    
    Arguments:
        dt {float} -- adım büyüklüğü (s)
        pvt {ZamanKonumHız} -- t zamanında zaman konum hız
        mu {float} -- Kütleçekimi Sabiti (m^3/s^2)

    Returns:
        {ZamanKonumHız} -- t+dt zamanında zaman konum hız
    """
    a = pvt.ivme(mu)

    tYeni  = pvt.t + dt
    rYeni  = pvt.r + pvt.v * dt
    vYeni  = pvt.v + a * dt

    return ZamanKonumHız(tYeni, rYeni[0], rYeni[1], vYeni[0], vYeni[1])


def hesapDöngüsüEuler(pvt0, tAdım, tSon):
    """
    Euler sayısal integrasyon metoduyla konum ve hız değerleri listesini hesaplar.
    """
    # ilk değerleri doldur
    numPvtList = [pvt0]

    t = numPvtList[0].t + tAdım
    while t<=tSon:
        pvtNum = eulerZamanKonumHız(tAdım, numPvtList[-1])
        numPvtList.append( pvtNum )

        t += tAdım
    
    return (numPvtList)

# *********** ana kod yapısı ***********

# başlangıç zamanı
t0 = 0
# bitiş zamanı (sn)
tSon = 6000 
# adım büyüklüğü (sn)
tAdım5  = 5
tAdım10 = 10
tAdım1  = 1

# başlangıç konum ve hız
pvt0 = ZamanKonumHız(t0, 0, 7000*1E3, 7.5*1E3, 0)


# Euler sayısal integrasyon verisini hesaplayan döngüyü çalıştır
eulPvtList5  = hesapDöngüsüEuler(pvt0, tAdım5, tSon)
eulPvtList10 = hesapDöngüsüEuler(pvt0, tAdım10, tSon)
eulPvtList1  = hesapDöngüsüEuler(pvt0, tAdım1, tSon)

# *********** grafikler ***********


# konum grafiği 
plt.plot( [pvt.r[0] for pvt in eulPvtList5], [pvt.r[1] for pvt in eulPvtList5], label="Euler (" + str(tAdım5) + " s)")

plt.title("Konum")
plt.xlabel("x konum (m)")
plt.ylabel('y konum (m)')

plt.axes().set_aspect('equal')
plt.grid(b=True, which='major', linestyle='--')

plt.show()

# hız grafiği
plt.plot( [pvt.v[0] for pvt in eulPvtList5], [pvt.v[1] for pvt in eulPvtList5], label="Euler (" + str(tAdım5) + " s)")

plt.title("Hız")
plt.xlabel("x hız (m/s)")
plt.ylabel("y hız (m/s)")

plt.axes().set_aspect('equal')
plt.grid(b=True, which='major', linestyle='--')

plt.show()

# enerji grafiği 

#referans değer - tüm farklar bu değere göre hesaplanacak
spEnerjiRef = pvt0.spesifikEnerji()

plt.title("Euler Spesifik Enerji Değişimi")
plt.xlabel("zaman (s)")
plt.ylabel("spesifik enerji ($m^2/s^2$)")

plt.plot( [pvt.t for pvt in eulPvtList1], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in eulPvtList1], label="Euler (" + str(tAdım1) + " s)")
plt.plot( [pvt.t for pvt in eulPvtList5], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in eulPvtList5], label="Euler (" + str(tAdım5) + " s)")
plt.plot( [pvt.t for pvt in eulPvtList10], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in eulPvtList10], label="Euler (" + str(tAdım10) + " s)")

plt.legend(loc=2)

plt.show()