# -*- coding: utf-8 -*-
"""
Serbest düşüş örneği v2.

Ay ile karşılaştırma.
"""
# sonradan gerekecek kütüphanelerini çağır
import matplotlib.pyplot as plt

# Kütleçekimi Sabiti [m/s^2]
gDünya = 9.81
gAy  = 1.625 

# bitiş zamanı (sn)
tSon = 10 
# adım büyüklüğü (sn)
tAdım = 0.5


# başlangıç zamanı, irtifa ve hız
t0 = 0 
h0 = 0
v0 = 0

# Zaman, yükseklik ve hız listelerini oluştur
tList = []
hListDünya = []
vListDünya = []
hListAy = []
vListAy = []


# Normal inline method
def h(t, h0=0, g=gDünya):
    """Verilen bir t zamanı için irtifayı döndürür ($ h(t) = h_0 - \frac{1}{2} g t^2 $)"""
    return h0 + (-1/2 * g * t**2)

# Lambda method
v = lambda t, vy0=0, g=gDünya: vy0 + ( -g*t )
#    """Verilen bir t zamanı için hızı döndürür ($ v(t) = v_0 - g t $)"""


t = t0 
while t<=tSon:
    hListDünya.append( h(t, h0, gDünya) )
    vListDünya.append( v(t, v0, gDünya) )
    
    hListAy.append( h(t, h0, gAy) )
    vListAy.append( v(t, v0, gAy) )
    
    tList.append(t)
    t += tAdım

# Zaman listesinin ilk 3 elemanını ekrana bas
print(tList[:3])
# Yükseklik listesinin ilk 3 elemanını ekrana bas
print(hListDünya[:3])
# Hız listesinin ilk 3 elemanını ekrana bas
print(vListDünya[:3])

# Yükseklik grafiği
plt.subplot(211)
plt.plot( tList , hListDünya, label="Dünya")
plt.plot( tList , hListAy, label="Ay")

plt.title(r"Yükseklik ve Hız Değişimi ($ h = \frac{1}{2} g t^2 $ & $ v = -gt $)")
plt.xlabel("zaman (s)")
plt.ylabel('yükseklik (m)')
plt.legend(loc=3)

# Hız grafiği
plt.subplot(212)
plt.plot( tList , vListDünya, label="Dünya")
plt.plot( tList , vListAy, label="Ay")

plt.xlabel("zaman (s)")
plt.ylabel("hız (m/sn)")
plt.legend(loc=3)

plt.show()