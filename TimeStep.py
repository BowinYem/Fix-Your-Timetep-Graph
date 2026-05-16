from collections.abc import Callable 

class TimeStepData:
    def __init__(self, function : Callable[[float], float] | Callable[[float, float], float], 
                 color : str, marker : str):
        self.function = function
        self.color = color
        self.marker = marker
    
def Integrate(p : Position, frameTime : float) -> None:
def Integrate(p : float, frameTime : float) -> float:
    velocity = 1
    p += (velocity * frameTime)
    return p

def FixedTimeStep(p : float) -> float:
    dt = 1.0 / 60.0
    p = Integrate(p, dt)
    return p    

def VariableTimeStep(p : float, frameTime : float) -> float:
    p = Integrate(p, frameTime)
    return p
    
def SemiFixedTimeStep(p : float, frameTime : float) -> float:
    dt = .016 # 1 / 60
    while(frameTime > 0.0):
        deltaTime = min(frameTime, dt)
        p = Integrate(p, deltaTime)
        frameTime -= deltaTime
    return p

def MixedTimeStep(p : float, frameTime : float) -> float:
    dt = 0.01

    if(frameTime > 0.25): # For spiral of death
        frameTime = 0.25

    MixedTimeStep.accumulator += frameTime
    
    while(MixedTimeStep.accumulator >= dt):
        MixedTimeStep.prevPos = p
        p = Integrate(p, dt)
        MixedTimeStep.accumulator -= dt

    alpha = MixedTimeStep.accumulator / dt
    interpolatedPos =  (p * alpha) + (MixedTimeStep.prevPos * (1.0 - alpha))
    return interpolatedPos
MixedTimeStep.accumulator = 0.0
MixedTimeStep.prevPos = 0.0


