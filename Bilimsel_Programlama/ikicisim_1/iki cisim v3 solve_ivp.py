# -*- coding: utf-8 -*-
"""
İki cisim problemi örneği v3.

scipy ode ve enum.

Hazırlayan: Egemen Imre, 2018
"""
# sonradan gerekecek kütüphaneleri çağır
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from enum import Enum

# Kütleçekimi Sabiti [m^3/s^2]
muDünya = 398600.5*1E9   

class ODEÇözücüTipi(Enum):
    """
    solve_ivp integrasyon tipleri
    """
    RK45 = 'RK45'
    RK23 = 'RK23'
    RADAU = 'Radau'
    BDF = 'BDF'
    LSODA = 'LSODA'

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
        mu {float} -- Kütleçekimi Sabiti (m^3/s^2) (default: {muDünya})

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

    Arguments:
        tAdım {float} -- adım büyüklüğü (s)
        pvt0 {ZamanKonumHız} -- başlangıç zamanında zaman konum hız
        tSon {float} -- bitiş zamanı (s)

    Returns:
        list {ZamanKonumHız} --  her bir zaman adımı için zaman konum hız değerlerini içeren liste
    """
    # ilk değerleri doldur
    numPvtList = [pvt0]

    t = numPvtList[0].t + tAdım
    while t<=tSon:
        pvtNum = eulerZamanKonumHız(tAdım, numPvtList[-1])
        numPvtList.append( pvtNum )

        t += tAdım
    
    return (numPvtList)


def odeDiffDenklem(t, y, mu=muDünya):
    """
    İki cisim problemi için diferansiyel denklem setini tanımlar.
    
    Arguments:
        t {float} -- başlangıç zamanı (s)
        y {ndarray} -- konum (m) ve hızı (m/s) içeren 1B, 4 elemanlı vektör [r_x r_y v_x v_y]


    Returns:
        {ndarray} -- konum ve hız diferansiyel denklemlerini (hız (m/s) ve ivmeyi(m/s^2)) içeren 
        1B, 4 elemanlı vektör [v_x v_y a_x a_y]
    """
    r = np.sqrt(y[0]**2 + y[1]**2)

    dy0 = y[2]
    dy1 = y[3]
    dy2 = -(mu / (r**3)) * y[0]
    dy3 = -(mu / (r**3)) * y[1]
    
    return [dy0, dy1, dy2, dy3]


    # r = np.sqrt(y[0]**2 + y[1]**2 + y[2]**2)

    # dy0 = y[3]
    # dy1 = y[4]
    # dy2 = y[5]
    # dy3 = -(mu / (r**3)) * y[0]
    # dy4 = -(mu / (r**3)) * y[1]
    # dy5 = -(mu / (r**3)) * y[2]

#    return [dy0, dy1, dy2, dy3, dy4, dy5]



def odeÇözümü(pvt0, tAdım, tSon, çözücüTipi = ODEÇözücüTipi.RK45):
    """
    Scipy ODE sayısal integrasyon metodlarıyla konum ve hız değerleri listesini hesaplar.

    Arguments:
        tAdım {float} -- adım büyüklüğü (s)
        pvt0 {ZamanKonumHız} -- başlangıç zamanında zaman konum hız
        tSon {float} -- bitiş zamanı (s)
        çözücüTipi {ODEÇözücüTipi} -- ODE Çözücü Tipi

    Returns:
        list {ZamanKonumHız} --  her bir zaman adımı için zaman konum hız değerlerini içeren liste
    """

    # adımSayısı ve zaman listesini oluştur
    adımSayısı = (tSon-pvt0.t)/tAdım + 1
    zamanListesi = np.asarray(np.linspace(pvt0.t, tSon, num = int(adımSayısı), endpoint=True))
    
    # diff denklem başlangıç değerlerini oluştur
    diffIlkDeğer = np.asarray(np.concatenate([pvt0.r, pvt0.v]))
    
    # diff denklemi başlangıç zamanından son zamana dek çöz
    diffDenkÇözüm = solve_ivp(odeDiffDenklem, [pvt0.t, tSon], diffIlkDeğer, method=çözücüTipi.value, dense_output=True, 
                                                                                        rtol = 1e-12, atol = 1e-15) 

#    print(diffDenkÇözüm)
#    print(diffDenkÇözüm.sol.__call__(0))
    
    # zaman listesine karşılık gelen değerleri oluştur
    cozumListesi = diffDenkÇözüm.sol.__call__(zamanListesi)
    
    # sonuç listesini başlat
    numPvtList = []

    # Listeyi objelere dönştür
    for i in range(len(zamanListesi)):
        pvArray = cozumListesi[:, i]
        numPvtList.append( ZamanKonumHız(zamanListesi[i], pvArray[0], pvArray[1], pvArray[2], pvArray[3]) )

    return (numPvtList)


# *********** ana kod yapısı ***********

# başlangıç zamanı
t0 = 0
# bitiş zamanı (sn)
tSon = 6000
# adım büyüklüğü (sn)
tAdımEuler_1  = 5
tAdımEuler_2  = 1
tAdımODE = 60
çözücüTipi1 = ODEÇözücüTipi.RK23
çözücüTipi2 = ODEÇözücüTipi.RK45

# başlangıç konum ve hız
pvt0 = ZamanKonumHız(t0, 0, 7000*1E3, 7.5*1E3, 0)


# Euler sayısal integrasyon verisini hesaplayan döngüyü çalıştır
eulPvtList5  = hesapDöngüsüEuler(pvt0, tAdımEuler_1, tSon)
eulPvtList1  = hesapDöngüsüEuler(pvt0, tAdımEuler_2, tSon)

çözücüPvtList1 = odeÇözümü(pvt0, tAdımODE, tSon, çözücüTipi1)
çözücüPvtList2 = odeÇözümü(pvt0, tAdımODE, tSon, çözücüTipi2)

# *********** grafikler ***********

# konum grafiği
plt.plot( [pvt.r[0] for pvt in çözücüPvtList2], [pvt.r[1] for pvt in çözücüPvtList2], label=çözücüTipi2.value + " (" + str(tAdımODE) + " s)")

plt.title("Konum")
plt.xlabel("x konum (m)")
plt.ylabel('y konum (m)')

plt.axes().set_aspect('equal')
plt.grid(b=True, which='major', linestyle='--')

plt.show()

# hız grafiği
plt.plot( [pvt.v[0] for pvt in çözücüPvtList2], [pvt.v[1] for pvt in çözücüPvtList2], label=çözücüTipi2.value + " (" + str(tAdımODE) + " s)")

plt.title("Hız")
plt.xlabel("x hız (m/s)")
plt.ylabel("y hız (m/s)")

plt.axes().set_aspect('equal')
plt.grid(b=True, which='major', linestyle='--')

plt.show() 

# enerji grafikleri

#referans değer - tüm farklar bu değere göre hesaplanacak
spEnerjiRef = pvt0.spesifikEnerji()

plt.title("Spesifik Enerji Değişimi")
plt.xlabel("zaman (s)")
plt.ylabel("spesifik enerji ($m^2/s^2$)")
plt.yscale('log')

plt.plot( [pvt.t for pvt in eulPvtList1], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in eulPvtList1], label="Euler (" + str(tAdımEuler_2) + " s)")
plt.plot( [pvt.t for pvt in eulPvtList5], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in eulPvtList5], label="Euler (" + str(tAdımEuler_1) + " s)")
plt.plot( [pvt.t for pvt in çözücüPvtList1], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in çözücüPvtList1], label=çözücüTipi1.value + " (" + str(tAdımODE) + " s)")
plt.plot( [pvt.t for pvt in çözücüPvtList2], [np.abs(pvt.spesifikEnerji()-spEnerjiRef) for pvt in çözücüPvtList2], label=çözücüTipi2.value + " (" + str(tAdımODE) + " s)")

plt.legend(loc=4)

plt.show()
