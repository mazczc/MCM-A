import numpy as np
import matplotlib.pyplot as plt

from multi import *

#####################ARGS#################

B0 = 10
S0 = 0.1
n = 0.45#cm
Sw = 0.038#cm
Ks = 312.77#cm/d
c = 10
Zr = 40#cm
Em = 0.16#cm
k = 0.38#cm
Yg = 0.9
R = 0.01
q = 0.001#/d
RU = 2#cm
RL = 0.5#cm
km = 0.85
Alphamax = 0.11#/d
Deltamax = 0.109#/d

Rho = 220#cm**2/g
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
species_dic = {}
for i in range(10):
	s = species(AlphaBase* (i*0.1 + 0.5), Sw* (i*0.1 + 0.5), Gamma0* (i*0.1 + 0.5), Beta* (i*0.1 + 0.5), 0.5 + i*0.05, 2.0, 0.5)
	species_dic[i] = s

s = species(0.11,0.038,0.391,0.009,0.85,2.0,0.5)
species_dic["Standard"] = s

s = species(0.11, 0.01, 0.20, 0.002, 0.5, 2.0, 0.1)
species_dic["Xiao Qiang"] = s

s = species(0.2, 0.1, 0.4, 0.004, 0.85, 2.0, 0.5)
species_dic["Zhang"] = s

s = species(0.11, 0.038,0.391,0.009,1,2.0,0.5)
species_dic["AlphaFix_Standard"] = s

Species = ["AlphaFix_Standard"]
GammaList = []
SwList0 = []
BList0 = []
AlphaList0 = []
AlphamaxList = []
RLlist = []
RUlist = []
kmlist = []
for choice in Species:
	# rand = 1
	BList0.append(B0/len(Species))#np.random.normal(1, 0.3))
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
DStart = 800
DEnd = 1400
I = [np.random.normal(1, 0.01) for i in range(Time)]

for day in range(Time):
	Rain = I[day]
	#cm/d
	if day%40 !=0 :
	#if day <= 800:
		Rain=0
	#I = 0
	#添加干旱
	if day in range(DStart, DEnd):
		Rain = 0.2*Rain
	
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

plt.plot(range(Time + 1), [np.sum(B) for B in BlistDrought],label='Drought Bio'+ str(Species))
plt.plot(range(Time + 1), SlistDrought , label='Drought Water'+ str(Species))
plt.plot(range(Time + 1), [Alpha[0] for Alpha in AlphalistDrought],label='Drought Alpha'+ str(Species))

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
	if day%40 !=0 :
	#if day <= 800:
		Rain=0
	#I = 0
	#添加干旱
	#if day in range(DStart, DEnd):
	#	Rain = 0.2*Rain
	
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

plt.plot(range(Time + 1), [np.sum(B) for B in BlistNormal],label='Normal Bio'+ str(Species))
plt.plot(range(Time + 1), SlistNormal, label='Normal Water'+ str(Species))
plt.plot(range(Time + 1), [Alpha[0] for Alpha in AlphalistNormal],label='Normal Alpha'+ str(Species))


Resistent = (np.sum(BlistNormal[DEnd]) - np.sum(BlistDrought[DEnd])) /np.sum(BlistNormal[DEnd])
Recover = (np.sum(BlistNormal[DEnd + 400]) - np.sum(BlistDrought[DEnd + 400])) /np.sum(BlistNormal[DEnd + 100])
print("Resistent:", Resistent, ",Recover:", Recover)
#print(BlistNormal)

plt.legend()
plt.show()
