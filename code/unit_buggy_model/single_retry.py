import numpy as np
import matplotlib.pyplot as plt

def Bupdate(B,S,Sw,K,Alpha,Beta):
	d = B* (Alpha *((S - Sw)/(K + S - Sw)) - Beta) if S >= Sw else -B*Beta
	B = B + d
	return B if B>=0.0005 else 0
    # 如果 B 很小，认为灭绝

def Supdate(B, S, I, Sw, K, Ks, c, Gamma , n , Zr):
	Sum = B* (Gamma*(S - Sw) / (K + S - Sw)) if S >= Sw else 0
	Sc = np.power(S, c)
	d = (I - Ks *Sc)/(n*Zr) - Sum
	return S + d

### Alpha（同化率）会随着降雨脉冲发生脉冲性变化，alpha , delta , deltastar 是用来模拟这一脉冲性变化的
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
###


### 化简式子后，可以缩减为3个参数 Alpha , Beta , Gamma ，其中 Beta , Gamma 不会发生脉冲性变化
def GetBeta(R, FL, Q):
	return R*(1 - FL) + Q

def GetGamma(Rho, FL, Em, N, Zr):
	return Rho*FL*Em/(N * Zr)

def GetConstantAlpha(Am, Rho, FL, Yg):
	return Am*Rho*FL*Yg

if __name__ == "__main__":
    ### 基准参数设置
    B0 = 10
    S0 = 0.2
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
    Gamma = GetGamma(Rho, FL, Em, n, Zr)
    Beta = GetBeta(R, FL, q)
    ### 

    ### 降雨量设置
    Time = 2000
    DStart = 700
    DEnd = 750
    I = [np.random.normal(1.5, 0.01) for i in range(Time)]
    ### 

    ### 有干旱情况下的模拟
    B=B0
    Alpha=Alphamax
    S = S0

    BlistDrought = [B]
    AlphalistDrought = [Alpha]
    SlistDrought = [S]
    RainDrought = [0]
    LastRain = 0

    for day in range(Time):
        Rain = I[day]
        #cm/d
        ### 离散降水（见Assumption）
        if day%5 !=0 :
            Rain=0
        ###
        #添加干旱
        if day in range(DStart, DEnd):
            Rain = 0.2*I[day]
        
        ### 单次更新计算
        DeltaStar = DeltaStarUpdate(Deltamax,RU,RL,LastRain)
        Delta = Deltaupdate(km,Alpha,Alphamax,DeltaStar)
        newAlpha=Alphaupdate(km,Alpha,Delta)
        newB=Bupdate(B,S,Sw,k,newAlpha,Beta)
        newS = Supdate(B, S, Rain, Sw, k, Ks, c, Gamma, n, Zr)
        ###
        ### 单次更新
        B = newB
        S = newS
        Alpha = newAlpha
        ###

        BlistDrought.append(B)
        AlphalistDrought.append(Alpha)
        SlistDrought.append(S)
        RainDrought.append(Rain)
        LastRain = Rain

    ###

    ### 无干旱情况下的模拟（作为对照组）
    B=B0
    Alpha=Alphamax
    S = S0

    BlistNormal = [B]
    AlphalistNormal = [Alpha]
    SlistNormal = [S]
    RainNormal = [0]
    LastRain = 0

    for day in range(Time):
        Rain = I[day]
        #cm/d
        if day%5 !=0 :
            Rain=0
        
        DeltaStar = DeltaStarUpdate(Deltamax,RU,RL,LastRain)
        Delta = Deltaupdate(km,Alpha,Alphamax,DeltaStar)
        newAlpha=Alphaupdate(km,Alpha,Delta)
        newB=Bupdate(B,S,Sw,k,newAlpha,Beta)
        newS = Supdate(B, S, Rain, Sw, k, Ks, c, Gamma, n, Zr)
        
        B = newB
        S = newS
        Alpha = newAlpha

        BlistNormal.append(B)
        AlphalistNormal.append(Alpha)
        SlistNormal.append(S)
        RainNormal.append(Rain)
        LastRain = Rain
    
    
    ### 借助比对，计算抵抗力稳定性和恢复力稳定性
    ### 目前：Resistent 越大，抵抗力越差
    ### Recover 越大，恢复力越差
    Resistent = (np.sum(BlistNormal[DEnd]) - np.sum(BlistDrought[DEnd])) /np.sum(BlistNormal[DEnd])
    Recover = (np.sum(BlistNormal[DEnd + 100]) - np.sum(BlistDrought[DEnd + 100])) /np.sum(BlistNormal[DEnd + 100])
    print("Resistent:", Resistent, ",Recover:", Recover)
    ###

    #for i in range(Num_species):
        #plt.plot(range(Time+1),[B[i] for B in BlistNormal] , label = 'Type'+str(i))
    
    # plt.plot(range(Time + 1), [B[0] for B in Blist],label='Type 1')
    # plt.plot(range(Time + 1), [B[1] for B in Blist],label='Type 2')
    plt.plot(range(Time + 1), [np.sum(B) for B in BlistNormal],label='Normal Bio')
    plt.plot(range(Time + 1), [np.sum(B) for B in BlistDrought], label = 'Drought Bio')
    # plt.plot(range(Time + 1), RainNormal,label='Normal Rain')
    # plt.plot(range(Time + 1), RainDrought, label = 'Drought Rain')
    plt.plot(range(Time + 1), SlistNormal,label='Normal S')
    plt.plot(range(Time + 1), SlistDrought, label = 'Drought S')
    plt.plot(range(Time + 1), AlphalistNormal,label='Normal Alpha')
    plt.plot(range(Time + 1), AlphalistDrought, label = 'Drought Alpha')
    # plt.plot(range(Time + 1), [Alpha[0] for Alpha in Alphalist],label='Alpha')
    # plt.plot(range(Time + 1), Slist,label='water')
    # plt.plot(range(Time + 1), Rains,label='Daily Rain')
    plt.legend()
    plt.show()