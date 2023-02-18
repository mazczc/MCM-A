import numpy as np
import matplotlib.pyplot as plt

def GetBeta(R, FL, Q):
	return R*(1 - FL) + Q

def GetGamma(Rho, FL, Em, N, Zr):
	return Rho*FL*Em/(N * Zr)

def GetConstantAlpha(Am, Rho, FL, Yg):
	return Am*Rho*FL*Yg

class Plant:
	def __init__(self,B,Sw,alpha,alphamax,beta,gamma,deltamax,K,Km,RL,RU,name):
		self.B=B				# 生物量
		self.Sw=Sw				# 枯萎阈值
		self.alpha=alpha 		# 当前同化作用速率
		self.alphamax=alphamax	# 最大同化作用速率
		self.beta=beta			# 凋亡速率（枯枝败叶生成等）
		self.gamma=gamma		# 蒸腾作用速率
		self.deltamax=deltamax	# 最大潜在增加
		self.K=K				# 半饱和系数（同化作用、蒸腾作用半饱和）
		self.Km=Km				# 响应衰减系数
		self.RL=RL				# 降水最小响应阈值
		self.RU=RU				# 降水最大响应阈值
		self.name=name			# 物种名称
	def Bupdate(self,S):
		d=self.B*(self.alpha*(S-self.Sw)/(self.K+S-self.Sw)-self.beta) if S>=self.Sw else -self.B*self.beta
		self.B+=d
	def Scost(self,S):
		return self.B*self.gamma*(S-self.Sw)/(self.K+S-self.Sw) if S>=self.Sw else 0
	def CalcAlphaupdate(self,Delta):
		self.alpha=self.alpha*self.Km+Delta
	def GetDelta(self,DeltaStar):
		Delta1=(1-self.Km)*self.alphamax
		Delta2=DeltaStar*(1-self.alpha/self.alphamax)
		return min(Delta1,Delta2)
	def GetDeltaStar(self,R):
		DeltaStar=self.deltamax*(R-self.RL)/(self.RU-self.RL)
		DeltaStar = min(max(DeltaStar, 0), self.deltamax) 
		return DeltaStar
	def Alphaupdate(self,R):
		DeltaStar=self.GetDeltaStar(R)
		Delta=self.GetDelta(DeltaStar)
		self.CalcAlphaupdate(Delta)

def Supdate(PlantList,S,I,c,Ks,n,Zr):
	Sum=0
	for plant in PlantList:
		Sum+=Plant.Scost(plant,S)
	Sc=np.power(S,c)
	delta=(I-Ks*Sc)/(n*Zr)-Sum
	return S+delta

def GetDayRain(day):
	I = np.random.normal(1.5, 0.01)#cm/d
	if day%5 !=0 :
		I=0
	#添加干旱
	if day%1500 in range(1000, 1500):
		I = 0.01*I
	return I

if __name__ == "__main__":
	StandardPlant=Plant(0.5,0.038,1.1,1.1,0.009,0.39,0.109,0.38,0.85,0.5,2,'0')
	###################################################
	# B0 = 0.5
	S0 = 0.1
	n = 0.45#cm
	# Sw = 0.038#cm
	Ks = 312.77#cm/d
	c = 10
	Zr = 40#cm
	# Em = 0.16#cm
	# k = 0.38#cm
	# Yg = 0.9
	# R = 0.01
	# q = 0.001#/d
	# RU = 2#cm
	# RL = 0.5#cm
	# km = 0.85
	# Alphamax = 1.1#/d
	# Deltamax = 0.109#/d
	# Rho = 220#cm**2/g
	# FL = 0.20
	###################################################

	#################################################################
	#这里我们搞几个不同的物种特征，每一个的Gamma， Sw， Rho 在一定范围内浮动？
	for Num_species in [8]:
		PlantList=[]
		BList=[]
		for i in range(Num_species):
			# rand = np.random.normal(1,0.1)
			# rand = 1
			PlantList.append(StandardPlant)
			# BList.append(B0*np.random.normal(1, 0.3))
			# SwList.append(Sw* rand)
			# GammaList.append(Gamma * rand)
			# AlphaList.append(GetConstantAlpha(0.028* rand, Rho, FL, Yg))
			# AlphamaxList.append(0.028*rand*Rho*FL*Yg)
		###############################################################
		for i in range(Num_species):
			BList.append(PlantList[i].B)
		Time = 50
		S = S0

		DayPlantList=[PlantList]
		DayRain=[0]
		DayWater=[S]

		for day in range(Time):

			I=GetDayRain(day)
			LastRain=DayRain[day]

			newPlantList=PlantList
			for i in range(len(PlantList)):
				newPlantList[i].Alphaupdate(LastRain)
				newPlantList[i].Bupdate(S)
			S=Supdate(PlantList,S,I,c,Ks,n,Zr)
			print([PlantList[i].B for i in range(Num_species)])
			PlantList=newPlantList
			DayPlantList.append(PlantList)
			DayRain.append(I)
			DayWater.append(S)
		
		for day in range(Time+1):
			print([PlantList[i].B for i in range(Num_species)])

		### output B of each kind of plant
		for i in range(Num_species):
			plt.plot(range(Time+1),[plantlist[i].B for plantlist in DayPlantList],label='B of Type '+PlantList[i].name)
		###
		### output total B 
		#plt.plot(range(Time + 1),[np.sum(B) for B in DayBList],label='Species = '+str(Num_species))
		###
		# plt.plot(range(Time + 1),DayWater,label='water')
		# plt.plot(range(Time + 1),DayRain,label='Daily Rain')
	plt.legend()
	plt.show()