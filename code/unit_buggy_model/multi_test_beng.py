import numpy as np
import matplotlib.pyplot as plt
import water

def Bupdate(B,S,Sw,K,Alpha,Beta):
	d = B* (Alpha *((S - Sw)/(K + S - Sw)) - Beta) if S >= Sw else -B*Beta
	B = B + d
	return B

def Supdate(BList, S, I, SwList, K, Ks, c, GammaList):
	Sum = 0
	for i in range(len(BList)):
		Sum += BList[i]* (GammaList[i]*(S - SwList[i]) / (K + S - SwList[i])) if S >= SwList[i] else 0
	Sc = np.power(S, c)
	d = I - Sum - Ks *Sc 
	return S + d

def Alphaupdate(Km, Alpha, Delta):
	return Alpha*Km + Delta

def Deltaupdate(K, Alpha, AlphaMax, DeltaStar):
	Delta1 = (1 - K) *AlphaMax
	Delta2 = DeltaStar* (1 - (Alpha/AlphaMax))
	return min(Delta1, Delta2)

def DeltaStarUpdate(DeltaMax, RU, RL, R):
	DeltaStar = DeltaMax * (R - RL)/(RU - RL)
	DeltaStar = min(max(DeltaStar, 0), DeltaMax) 
	return DeltaStar

def GetBeta(R, FL, Q):
	return R*(1 - FL) + Q

def GetGamma(Rho, FL, Em, N, Zr):
	return Rho*FL*Em/(N * Zr)

def GetConstantAlpha(Am, Rho, FL, Yg):
	return Am*Rho*FL*Yg

if __name__ == "__main__":
	IsBeng = True
	B = 2.25
	S0 = 0.15
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
	Alphamax = 1.1#/d
	Deltamax = 0.109#/d

	Rho = 220#cm**2/g
	FL = 0.20

	#################################################################
	#这里我们搞几个不同的物种特征，每一个的Gamma， Sw， Rho 在一定范围内浮动？
	Num_species = 7
	GammaList = []
	Gamma = GetGamma(Rho, FL, Em, n, Zr)
	Beta = GetBeta(R, FL, q)
	SwList = []
	BList = []
	AmList = []
	for i in range(Num_species):
		BList.append(2.25/Num_species*np.random.normal(1, 0.3))
		rand = np.random.normal(1, 0.01)
		SwList.append(Sw* rand)
		GammaList.append(Gamma * rand)
		AmList.append(0.00075*rand)
	###############################################################

	Time = 10000

	Blist = [BList]
	S = S0
	Slist = [S]

	

	for day in range(Time):

		I = np.random.normal(0.3, 0.05)#cm/d
		if I < 0:
			I = 0

		#添加干旱
		if day%360 in range(100, 200):
			I = 0.1* I
		newBlist = []
		for i in range(len(BList)):
			Alpha = GetConstantAlpha(AmList[i], Rho, FL, Yg)
			newBlist.append(Bupdate(BList[i],S,SwList[i],k,Alpha,Beta))
		newS = Supdate(BList, S, I, SwList, k, Ks, c, GammaList)
		BList = newBlist
		S = newS
		if np.sum(BList) < 0.5 :
			
			if IsBeng:
				print("崩了，在", day)
			IsBeng = False
			
		Blist.append(BList)
		Slist.append(S)
	if IsBeng == True:
		print("居然没崩")

	#for i in range(len(Blist[0])):
		#plt.plot(range(Time + 1), [B[i] for B in Blist])
	#plt.plot(range(Time + 1), [np.sum(B) for B in Blist])

	#plt.show()

	BengTime = []

	for i in range(100):

		SwList = []
		BList = []
		AmList = []
		for i in range(Num_species):
			BList.append(2.25/Num_species*np.random.normal(1, 0.3))
			rand = np.random.normal(1, 0.01)
			SwList.append(Sw* rand)
			GammaList.append(Gamma * rand)
			AmList.append(0.00075*rand)
		S = S0
		IsBeng = True
		for day in range(Time):

			I = np.random.normal(0.3, 0.05)#cm/d
			if I < 0:
				I = 0

			#添加干旱
			if day%360 in range(100, 200):
				I = 0.1* I
			newBlist = []
			for i in range(len(BList)):
				Alpha = GetConstantAlpha(AmList[i], Rho, FL, Yg)
				newBlist.append(Bupdate(BList[i],S,SwList[i],k,Alpha,Beta))
			newS = Supdate(BList, S, I, SwList, k, Ks, c, GammaList)
			BList = newBlist
			S = newS
			if np.sum(BList) < 0.5 :
				if IsBeng:
					print("崩了，在", day)
					IsBeng = False
					BengTime.append(day)
			
			Blist.append(BList)
			Slist.append(S)
		if IsBeng == True:
			print("居然没崩")
			BengTime.append(1.5*Time)
		
	print(BengTime)
	print(np.sum(BengTime)/len(BengTime))