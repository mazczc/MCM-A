import numpy as np
import matplotlib.pyplot as plt
import water

def Bupdate(B,S,Sw,K,Alpha,Beta):
	d = B* (Alpha *((S - Sw)/(K + S - Sw)) - Beta) if S >= Sw else -B*Beta
	B = B + d
	return B if B>=0.0005 else 0
	#return B

def Supdate(BList, S, I, SwList, K, Ks, c, GammaList , n , Zr):
	Sum = 0
	for i in range(len(BList)):
		Sum += BList[i]* (GammaList[i]*(S - SwList[i]) / (K + S - SwList[i])) if S >= SwList[i] else 0
	Sc = np.power(S, c)
	d = (I - Ks *Sc)/(n*Zr) - Sum
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
	B0 = 0.5
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
	Alphamax = 1.1#/d
	Deltamax = 0.109#/d

	Rho = 220#cm**2/g
	FL = 0.20

	#################################################################
	#这里我们搞几个不同的物种特征，每一个的Gamma， Sw， Rho 在一定范围内浮动？
	for Num_species in [4, 6, 8]:
		GammaList = []
		Gamma = GetGamma(Rho, FL, Em, n, Zr)
		Beta = GetBeta(R, FL, q)
		SwList0 = []
		BList0 = []
		AlphaList0 = []
		AlphamaxList = []
		for i in range(Num_species):
			rand = np.random.normal(1,0.1)
			# rand = 1
			BList0.append(B0/Num_species*np.random.normal(1, 1))
			SwList0.append(Sw* rand)
			GammaList.append(Gamma * rand)
			AlphaList0.append(GetConstantAlpha(0.028* rand, Rho, FL, Yg))
			AlphamaxList.append(0.028*rand*Rho*FL*Yg)
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
		DStart = 700
		DEnd = 750
		I = [np.random.normal(1.5, 0.01) for i in range(Time)]

		for day in range(Time):
			Rain = I[day]
			#cm/d
			if day%5 !=0 :
			#if day <= 800:
				Rain=0
			#I = 0
			#添加干旱
			if day in range(DStart, DEnd):
				Rain = 0.2*I[day]
			
			newBlist = []
			newAlphaList = []
			LastRain = Rains[day]
			DeltaStar = DeltaStarUpdate(Deltamax,RU,RL,LastRain)
			for i in range(len(BList)):
				Delta = Deltaupdate(km,AlphaList[i],AlphamaxList[i],DeltaStar)
				newAlphaList.append(Alphaupdate(km,AlphaList[i],Delta))
				newBlist.append(Bupdate(BList[i],S,SwList[i],k,newAlphaList[i],Beta))
			
			newS = Supdate(BList, S, Rain, SwList, k, Ks, c, GammaList, n, Zr)
			BList = newBlist
			AlphaList = newAlphaList
			S = newS
			BlistDrought.append(BList)
			AlphalistDrought.append(AlphaList)
			SlistDrought.append(S)
			Rains.append(Rain)


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
			if day%5 !=0 :
			#if day <= 1800:
				Rain=0
			#添加干旱
			#if day in range(1000, 1500):
				#I = 0.03*I
			
			newBlist = []
			newAlphaList = []
			LastRain = Rains[day]
			DeltaStar = DeltaStarUpdate(Deltamax,RU,RL,LastRain)
			for i in range(len(BList)):
				Delta = Deltaupdate(km,AlphaList[i],AlphamaxList[i],DeltaStar)
				newAlphaList.append(Alphaupdate(km,AlphaList[i],Delta))
				newBlist.append(Bupdate(BList[i],S,SwList[i],k,newAlphaList[i],Beta))
			
			newS = Supdate(BList, S, Rain, SwList, k, Ks, c, GammaList, n, Zr)
			BList = newBlist
			AlphaList = newAlphaList
			S = newS
			BlistNormal.append(BList)
			AlphalistNormal.append(AlphaList)
			SlistNormal.append(S)
			Rains.append(Rain)

		Resistent = (np.sum(BlistNormal[DEnd]) - np.sum(BlistDrought[DEnd])) /np.sum(BlistNormal[DEnd])
		Recover = (np.sum(BlistNormal[DEnd + 100]) - np.sum(BlistDrought[DEnd + 100])) /np.sum(BlistNormal[DEnd + 100])
		print("Resistent:", Resistent, ",Recover:", Recover)

		#for i in range(Num_species):
			#plt.plot(range(Time+1),[B[i] for B in BlistNormal] , label = 'Type'+str(i))
		
		# plt.plot(range(Time + 1), [B[0] for B in Blist],label='Type 1')
		# plt.plot(range(Time + 1), [B[1] for B in Blist],label='Type 2')
		plt.plot(range(Time + 1), [np.sum(B) for B in BlistNormal],label='Normal'+ str(Num_species))
		plt.plot(range(Time + 1), [np.sum(B) for B in BlistDrought], label = 'Drought'+ str(Num_species))
		# plt.plot(range(Time + 1), [Alpha[0] for Alpha in Alphalist],label='Alpha')
		# plt.plot(range(Time + 1), Slist,label='water')
		# plt.plot(range(Time + 1), Rains,label='Daily Rain')
	plt.legend()
	plt.show()
	