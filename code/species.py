import numpy as np
import matplotlib.pyplot as plt

from multi import *

np.random.seed(1919810)

#####################ARGS#################

B0 = 8000
S0 = 0.1
n = 0.45#cm
Sw = 0.038#cm
Ks = 312.77#cm/d
c = 10
Zr = 40#cm
Em = 0.16#cm
k = 0.2#cm
Yg = 0.9
R = 0.01
q = 0.001#/d
RU = 2#cm
RL = 0.5#cm
km = 0.85
Alphamax = 1.1#/d
Deltamax = 0.109#/d

Rho = 0.022#cm**2/g
FL = 0.20

Gamma0 =  GetGamma(Rho, FL, Em, n, Zr)
Beta = GetBeta(R, FL, q)
AlphaBase = GetConstantAlpha(0.028, Rho, FL, Yg)

class species:
	def __init__(self, Alpha0, Sw, Gamma, Beta, km, RU, RL):
		self.Alpha = Alpha0
		self.Sw = Sw
		self.Beta = Beta
		self.Gamma = Gamma
		self.km = km
		self.RU = RU
		self.RL = RL

#####################################################
#这里可以任意添加新的物种进去，目前只有几个奇形怪状的东西
#####################################################
print(AlphaBase, Sw, Gamma0, Beta, 0.85, 2.0, 0.5)
species_dic = {}
for i in range(10):
	s = species(AlphaBase* (i*0.1 + 0.5), Sw* (i*0.035 + 0.3), Gamma0* (i*0.1 + 0.5), Beta* (-i*0.1 + 0.5), 0.85*(i*0.01 + 0.95), 2.0, 0.5)
	species_dic[i] = s



s = species(0.0308, 0.01, 1.0018e-5 ,0.0065, 1, 2.0, 0.5)
species_dic["A"] = s

s = species(0.051, 0.049, 1.0018e-5 ,0.0145, 1, 2.0, 0.5)
species_dic["B"] = s

s = species(0.0643, 0.06, 1.5418e-5 ,0.0095, 1, 2.0, 0.5)
species_dic["C"] = s

s = species(0.0643, 0.06, 2.5418e-5 ,0.0095, 1, 2.0, 0.5)
species_dic["Cw"] = s

s = species(0.065,0.061,1.5618e-5, 0.0098, 1, 2, 0.5)
species_dic["D"] = s

s = species(0.075, 0.065, 1.6418e-5 ,0.01, 1, 2.0, 0.5)
species_dic["E"] = s

s = species(0.08, 0.067, 1.6318e-5, 0.013, 1, 2.0, 0.5)
species_dic["F"] = s

s = species(0.1,0.072,1.7538e-5,0.009,1,2.0,0.5)
species_dic["G"] = s

s = species(0.15, 0.081, 2.5418e-5 ,0.0230, 1, 2.0, 0.5)
species_dic["H"] = s
 
Species = ["B", "B"]
GammaList = []
SwList0 = []
BList0 = [B0 / 3, B0*2/3]
AlphaList0 = []
AlphamaxList = []
RLlist = []
RUlist = []
kmlist = []
for choice in Species:
	# rand = 1
	#BList0.append(B0/len(Species))
	SwList0.append(species_dic[choice].Sw)
	GammaList.append(species_dic[choice].Gamma)
	AlphaList0.append(species_dic[choice].Alpha)
	AlphamaxList.append(Alphamax)
	RLlist.append(species_dic[choice].RL)
	RUlist.append(species_dic[choice].RU)
	kmlist.append(species_dic[choice].km)
###############################################################
S = S0
BList = BList0
SwList = SwList0
AlphaList = AlphaList0

BlistDrought = [BList]
AlphalistDrought = [AlphaList]
SlistDrought = [S]
Rains = [0]

Time = 2000
DStart = 1000
DEnd = 1090
I = [np.random.normal(0.3, 0.1) for i in range(Time)]
rand = [np.random.rand() for i in range(Time)]
droughtrand = [np.random.rand() for i in range(Time)]

for day in range(Time):
	Rain = I[day]
	#cm/d
	#if rand[day] > 0.202 :
	#if day%5 != 0:
	#if day <= 800:
		#Rain=0
	#I = 0
	#添加干旱
	#if day in range(DStart, DEnd):
		#Rain = 0.1*Rain
	if day in range(DStart, DEnd):
		Rain = 0.2 * Rain

	#if day in range(900, 950):
	#	Rain = 0.3 * Rain

	#if droughtrand[day] > 0.6:
	#	Rain = Rain*(1 - droughtrand[day])

	#if day in range(1200, 1250):
	#	Rain = 0.4*Rain	
	newBlist = []
	newAlphaList = []
	LastRain = Rains[day]
	
	for i in range(len(BList)):
		DeltaStar = DeltaStarUpdate(Deltamax,RUlist[i],RLlist[i],LastRain)
		Delta = Deltaupdate(kmlist[i],AlphaList[i],AlphamaxList[i],DeltaStar)
		newAlphaList.append(Alphaupdate(kmlist[i],AlphaList[i],Delta))
		newBlist.append(Bupdate(BList[i],S,SwList[i],k,newAlphaList[i],Beta))
	
	newS = Supdate(BList, S, Rain, SwList, k, Ks, c, GammaList, n, Zr)
	BList = newBlist
	AlphaList = newAlphaList
	S = newS
	BlistDrought.append(BList)
	AlphalistDrought.append(AlphaList)
	SlistDrought.append(S)
	Rains.append(Rain)

plt.plot(range(Time + 1), [np.sum(B) for B in BlistDrought],label='Drought'+ str(Species))

S = S0
BList = BList0
SwList = SwList0
AlphaList = AlphaList0

BlistNormal = [BList]
AlphalistNormal = [AlphaList]
SlistNormal = [S]
Rains = [0]

for day in range(Time):
	Rain = I[day]
	#cm/d
	#if rand[day] > 0.202 :
	#if day%5 != 0:
	#if day <= 800:
		#Rain=0
	#I = 0
	#添加干旱
	#if day in range(DStart, DEnd):
	#	Rain = 0.2*I[day]
	
	newBlist = []
	newAlphaList = []
	LastRain = Rains[day]
	for i in range(len(BList)):
		DeltaStar = DeltaStarUpdate(Deltamax,RUlist[i],RLlist[i],LastRain)
		Delta = Deltaupdate(kmlist[i],AlphaList[i],AlphamaxList[i],DeltaStar)
		newAlphaList.append(Alphaupdate(kmlist[i],AlphaList[i],Delta))
		newBlist.append(Bupdate(BList[i],S,SwList[i],k,newAlphaList[i],Beta))

	newS = Supdate(BList, S, Rain, SwList, k, Ks, c, GammaList, n, Zr)
	BList = newBlist
	AlphaList = newAlphaList
	S = newS
	BlistNormal.append(BList)
	AlphalistNormal.append(AlphaList)
	SlistNormal.append(S)
	Rains.append(Rain)

plt.plot(range(Time + 1), [np.sum(B) for B in BlistNormal],label='Total')

for i in range(len(BlistNormal[0])):
	plt.plot(range(Time+1),[B[i] for B in BlistNormal] , label = 'Type'+str(i))

for i in range(len(BlistDrought[0])):
	plt.plot(range(Time+1),[B[i] for B in BlistDrought] , label = 'TypeD'+str(i))

Resistent = (np.sum(BlistNormal[DEnd]) - np.sum(BlistDrought[DEnd])) /np.sum(BlistNormal[DEnd])
Recover = (np.sum(BlistNormal[DEnd + 100]) - np.sum(BlistDrought[DEnd + 100])) /np.sum(BlistNormal[DEnd + 100])
print("Resistent:", 1/Resistent, ",Recover:",1/ Recover)
print(AlphaList)

#plt.plot(range(Time+1),SlistNormal , label = 'S')

plt.legend()
plt.savefig("4species-normal-cycle_rain-['Xiao Qiang','D', 'New', 'standard']-with_total.png")
#plt.show()