from collections.abc import Callable 
from matplotlib.lines import Line2D
from integratefunc import Integrate
from integratefunc import IntegrateEnum
class TimeStepData:
    def __init__(self, function : Callable[[float, IntegrateEnum, float], float], 
                 line : Line2D):
        self.function = function
        self.line = line

def FixedTimeStep(p : float, integrationFunc : IntegrateEnum, frameTime : float = 0.0) -> float:
    # Note: frameTime parameter not used in this function - frameTime defined in order to be uniform with the other time step functions
    dt = 1.0 / 60.0
    p = Integrate(p, dt, integrationFunc)
    return p    

def VariableTimeStep(p : float, integrationFunc : IntegrateEnum, frameTime : float) -> float:
    p = Integrate(p, frameTime, integrationFunc)
    return p
    
def SemiFixedTimeStep(p : float, integrationFunc : IntegrateEnum, frameTime : float) -> float:
    dt = .016 # 1 / 60
    while(frameTime > 0.0):
        deltaTime = min(frameTime, dt)
        p = Integrate(p, deltaTime, integrationFunc)
        frameTime -= deltaTime
    return p

def MixedTimeStep(p : float, integrationFunc : IntegrateEnum, frameTime : float) -> float:
    dt = 0.01

    if(frameTime > 0.25): # For spiral of death
        frameTime = 0.25

    MixedTimeStep.accumulator += frameTime
    
    while(MixedTimeStep.accumulator >= dt):
        MixedTimeStep.prevPos = p
        p = Integrate(p, dt, integrationFunc)
        MixedTimeStep.accumulator -= dt

    alpha = MixedTimeStep.accumulator / dt
    interpolatedPos =  (p * alpha) + (MixedTimeStep.prevPos * (1.0 - alpha))
    return interpolatedPos
MixedTimeStep.accumulator = 0.0
MixedTimeStep.prevPos = 0.0


