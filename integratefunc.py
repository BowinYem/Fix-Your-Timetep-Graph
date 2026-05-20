from enum import IntEnum

class IntegrateEnum(IntEnum):
    LINEAR_INTG = 0
    SPRING_INTG = 1

DAMPING = 0
SPRING_CONST = 20
MASS = 1  

velocity = 0

def LinearIntegrate(p : float, frameTime : float) -> float:
    global velocity
    velocity = 1
    p += (velocity * frameTime)
    return p

def SpringIntegrate(p : float, frameTime : float) -> float:
    global velocity
    acceleration = -((DAMPING * velocity) + (SPRING_CONST * p)) / MASS
    velocity += acceleration * frameTime
    p += velocity * frameTime
    return p   

def Integrate(p : float, frameTime : float, integrationFunc : IntegrateEnum) -> float:
    return Integrate.functions[integrationFunc](p, frameTime)
Integrate.functions = [] 
Integrate.functions.append(LinearIntegrate)
Integrate.functions.append(SpringIntegrate)
