import numpy as np
import matplotlib.pyplot as plt

def Bupdate(B,S,Sw,K,Alpha,Beta):
	d = B* (Alpha *((S - Sw)/(K + S - Sw)) - Beta) if S >= Sw else -B*Beta
	B = B + d
	return B

def Supdate(B, S, I, Sw, K, Ks, c, Gamma):
	Sc = np.power(S, c)
	d = I - B* (Gamma*(S - Sw) / (K + S - Sw)) - Ks *Sc if S >= Sw else I - Ks*Sc
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
	B = 2.25
	S = 0.15
	n = 0.45#cm
	Sw = 0.038#cm
	Ks = 312.77#cm/d
	c = 10
	Zr = 40#cm
	Em = 0.16#cm
	k = 0.38#cm
	Rho = 220#cm**2/g
	FL = 0.20
	Yg = 0.9
	R = 0.01
	q = 0.001#/d
	RU = 2#cm
	RL = 0.5#cm
	km = 0.85
	Alphamax = 1.1#/d
	Deltamax = 0.109#/d

	#########################################
	#此处口胡一个Am的值
	Am = 0.001#g/cm**2 #Am= 0.01时会炸

	Time = 1000
	#########################################

	Blist = [B]
	Slist = [S]

	Alpha = GetConstantAlpha(Am, Rho, FL, Yg)
	Beta = GetBeta(R, FL, q)
	Gamma = GetGamma(Rho, FL, Em, n, Zr)
	print(Beta)

	for day in range(Time):
		I = np.random.normal(0.2, 0.01)#cm/d
####################################################################
		#添加干旱
		#if day in range(200, 1000):
		#	I = 0.4* I
####################################################################
		newB = Bupdate(B,S,Sw,k,Alpha,Beta)
		newS = Supdate(B, S, I, Sw, k, Ks, c, Gamma)
		B = newB
		S = newS
		Blist.append(B)
		Slist.append(S)

	print(Blist)
	print(Slist)

	plt.plot(range(Time + 1), Blist)
	plt.plot(range(Time+ 1), Slist)
	plt.show()