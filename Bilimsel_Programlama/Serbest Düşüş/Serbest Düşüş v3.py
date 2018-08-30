import matplotlib.pyplot as plt

#Initial, constant and sampling values
gForWorld=9.81
gForMoon=1.625

tSamplingEnd = 10 #t, sec
tSamplingRate = 0.5 #t, sec

time=time0 = 0
height0 = 0
velocity0 = 0

#To keep sampled values together in an object
#Thanks to this, we can create different objects for different planets :)
class FallingObjectClass():
	def __init__(self,gPlanet,v0,h0):
		self.g=gPlanet
		self.v0=v0
		self.h0=h0
		self.vList=[] #To store last v values
		self.hList=[] #To store last h values

	def calculateVelocity(self,time):
		currentV = self.v0 - (self.g*time)
		self.vList.append(currentV)

	def calculateHeight(self,time):
		currentH=self.h0 + ((1/2)*-(self.g)*(time**2))
		self.hList.append(currentH)

	def calculateAllValues(self,time):
		self.calculateHeight(time)
		self.calculateVelocity(time)

#We create our objects which will be falling
objectInTheWorld = FallingObjectClass(gForWorld,velocity0,height0)
objectInTheMoon = FallingObjectClass(gForMoon,velocity0,height0)

tList= []

while time<tSamplingEnd:
	tList.append(time)
	objectInTheWorld.calculateAllValues(time)
	objectInTheMoon.calculateAllValues(time)	
	time+=tSamplingRate

plt.subplot(211)
plt.plot(tList, objectInTheWorld.hList, label="The World")
plt.plot(tList, objectInTheMoon.hList, label="The Moon")
plt.title("Position graph...");
plt.xlabel("Time (s)")
plt.ylabel('Height (m)')
plt.legend(loc=3)

plt.subplot(212)
plt.plot(tList, objectInTheWorld.vList, label="The World")
plt.plot(tList, objectInTheMoon.vList, label="The Moon")
plt.title("Velocity graph...");
plt.xlabel("Time (s)")
plt.ylabel('Velocity (m)')
plt.legend(loc=3)

plt.show()