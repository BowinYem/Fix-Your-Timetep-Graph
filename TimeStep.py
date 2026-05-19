from collections.abc import Callable 
from matplotlib.lines import Line2D

class TimeStepData:
    def __init__(self, function : Callable[[float], float] | Callable[[float, float], float], 
                 line : Line2D):
        self.function = function
        self.line = line

damping = 0
springConst = 20
mass = 1
def SpringIntegrate(p : float, frameTime : float) -> float:
    acceleration = -((damping * SpringIntegrate.velocity) + (springConst * p)) / mass
    SpringIntegrate.velocity += acceleration * frameTime
    p += SpringIntegrate.velocity * frameTime
    return p      
SpringIntegrate.velocity = 0

def LinearIntegrate(p : float, frameTime : float) -> float:
    velocity = 1
    p += (velocity * frameTime)
    return p

def FixedTimeStep(p : float) -> float:
    dt = 1.0 / 60.0
    p = SpringIntegrate(p, dt)
    return p    

def VariableTimeStep(p : float, frameTime : float) -> float:
    p = SpringIntegrate(p, frameTime)
    return p
    
def SemiFixedTimeStep(p : float, frameTime : float) -> float:
    dt = .016 # 1 / 60
    while(frameTime > 0.0):
        deltaTime = min(frameTime, dt)
        p = SpringIntegrate(p, deltaTime)
        frameTime -= deltaTime
    return p

def MixedTimeStep(p : float, frameTime : float) -> float:
    dt = 0.01

    if(frameTime > 0.25): # For spiral of death
        frameTime = 0.25

    MixedTimeStep.accumulator += frameTime
    
    while(MixedTimeStep.accumulator >= dt):
        MixedTimeStep.prevPos = p
        p = SpringIntegrate(p, dt)
        MixedTimeStep.accumulator -= dt

    alpha = MixedTimeStep.accumulator / dt
    interpolatedPos =  (p * alpha) + (MixedTimeStep.prevPos * (1.0 - alpha))
    return interpolatedPos
MixedTimeStep.accumulator = 0.0
MixedTimeStep.prevPos = 0.0


