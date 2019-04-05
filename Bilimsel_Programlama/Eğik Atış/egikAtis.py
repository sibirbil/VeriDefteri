import matplotlib.pyplot as plt
import math

gForWorld=9.81
gForMoon=1.625

class VelocityVector():
	def __init__(self,v0,angle,gPlanet):
		self.g=gPlanet
		self.v0=v0
		self.angle=angle
		self.v0x=v0*math.cos(math.radians(angle))
		self.v0y=v0*math.sin(math.radians(angle))
		print(self.v0x, "", self.v0y)

	def calculateNewVelocityVector(self,time):
		new_v0y=self.v0y-(self.g*time)
		new_angle=math.degrees(math.atan(new_v0y/self.v0x))
		new_v0=new_v0y/(math.sin(math.radians(new_angle)))

		return VelocityVector(new_v0,new_angle,self.g)

class ProjectileMotionObject():
	def __init__(self, gPlanet, v0, angle,x0,y0):
		self.x0=x0
		self.y0=y0
		self.g=gPlanet
		self.xLast=x0
		self.yLast=y0
		self.velocityVector=VelocityVector(v0,angle,gPlanet)
		self.vList=[]
		self.lList=[]
		self.tList=[]

	def calculateVelocity(self,time):
		currentV = self.velocityVector.calculateNewVelocityVector(time)
		self.vList.append(currentV)

	def calculateLocation(self,time):
		self.xLast=self.x0 + (self.velocityVector.v0x*time)
		self.yLast=self.y0 + (self.velocityVector.v0y*time) + (-1/2*self.g*(time**2))
		self.lList.append((self.xLast,self.yLast))

	def calculateAllValues(self,time):
		self.tList.append(time)
		self.calculateVelocity(time)
		self.calculateLocation(time)

	def getListOfXLoc(self):
		return [value[0] for value in self.lList]

	def getListOfYLoc(self):
		return [value[1] for value in self.lList]

projectileMotionObject=ProjectileMotionObject(gForWorld,100,50,0,0)

time=0
tSamplingRate=0.5
tEnd=50

while time<tEnd and projectileMotionObject.yLast>=0:
	projectileMotionObject.calculateAllValues(time)
	time+=tSamplingRate

f= plt.figure(1)

xAndTime=plt.subplot(221)
xAndTime.set_xlabel("Time")
xAndTime.set_ylabel("X Distance")
xAndTime.plot(projectileMotionObject.tList,projectileMotionObject.getListOfXLoc())

yAndTime=plt.subplot(222)
yAndTime.set_xlabel("Time")
yAndTime.yaxis.set_label_position("right")
yAndTime.set_ylabel("Y Distance")
yAndTime.plot(projectileMotionObject.tList,projectileMotionObject.getListOfYLoc())

xAndy=plt.subplot(212)
xAndy.set_xlabel("X Distance")
xAndy.set_ylabel("Y Distance")
xAndy.plot(projectileMotionObject.getListOfXLoc(),projectileMotionObject.getListOfYLoc())

plt.show()