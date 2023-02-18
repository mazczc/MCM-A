import numpy as np

WATERNEED = 10

def BioStep(Biomass, coeffiencients):
	#Biomass: 生物量数组，nparray, 依次对应物种i的生物量
	#coeffiencients: 生物影响关系矩阵，+代表促进，-代表竞争互相挤压
	Delta = np.dot(Biomass, coeffiencients)
	return Biomass + Delta

def WeatherStep(Biomass, Resistence ,Rain):
	#Biomass: 同上
	#Resistence: 对应的物种对干旱的抵抗能力
	#Rain: 当段时间的降水
	Delta = np.tanh((Rain*Resistence - np.sum(Biomass) * 10)* 0.01)
	print(Delta)
	return Biomass + Delta

class Environment:
	def __init__(self,num_species,species, coeffiencients):
		self.num_species = num_species
		self.species = species
		self.coeffiencients = coeffiencients

	def initialize(self):
		##################################################
		#Not Implemented
		##################################################
		return

	def Step(self, rainfall):
		##################################################
		#Not Implemented
		##################################################
		return
	
class Species:
	def __init__(self, Resistence, args = None):
		self.Resistence = Resistence
		self.args = args

	def WeatherAct(self, Rain):
		###################################################
		#Not Implements
		###################################################
		return

def Weather(ExpRain, VarRain ,IsDrought):
	rainfall = np.random.normal(ExpRain, VarRain)
	if IsDrought:
		return 0.1*rainfall
	else:
		return rainfall

def SigalDrought(ExpRain, VarRain, T, DroughtStart,DroughtEnd):
	Rain = []
	for t in range(T):
		IsDrought = (t in range(DroughtStart, DroughtEnd))
		rainfall = Weather(ExpRain, VarRain, IsDrought)
		Rain.append(rainfall)
	return Rain

if __name__ == "__main__":
	EXP = 792
	VAR = 10 
	T = 20
	START = 100
	END = 100
	Rain = SigalDrought(EXP,VAR,T, START, END)

	BioMass = np.array([10,10,10])
	Process = [BioMass]
	Res = np.array([0.3, 0.45, 0.5])
	Coe = np.array([[0,0.05,-0.1], [0.05,0,0.05], [-0.01,0.05,0]])

	for i in range(T):
		BioMass = BioStep(BioMass, Coe)
		BioMass = WeatherStep(BioMass, Res, Rain[i])
		Process.append(BioMass)

	print(np.array(Process))

	
