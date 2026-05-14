from collections.abc import Callable 
from Pos import Position

class TimeStepData:
    def __init__(self, function : Callable[[Position], Position] | Callable[[Position], None], 
                 color : str, marker : str):
        self.function = function
        self.color = color
        self.marker = marker
    
def Integrate(p : Position, frameTime : float) -> None:
    velocity = 1
    p.x += (velocity * frameTime)
    p.y += (velocity * frameTime)

def FixedTimeStep(p : Position) -> Position:
    dt = 1.0 / 60.0
    Integrate(p, dt)
    return p    

def VariableTimeStep(p : Position, frameTime : float) -> Position:
    Integrate(p, frameTime)
    return p
    
def SemiFixedTimeStep(p : Position, frameTime : float) -> Position:
    dt = .016 # 1 / 60
    while(frameTime > 0.0):
        deltaTime = min(frameTime, dt)
        Integrate(p, deltaTime)
        frameTime -= deltaTime
    return p

def MixedTimeStep(p : Position, frameTime : float) -> Position:
    dt = 0.01

    if(frameTime > 0.25): # For spiral of death
        frameTime = 0.25

    MixedTimeStep.accumulator += frameTime
    
    while(MixedTimeStep.accumulator >= dt):
        MixedTimeStep.prevPos = Position(p.x, p.y)
        Integrate(p, dt)
        MixedTimeStep.accumulator -= dt

    alpha = MixedTimeStep.accumulator / dt
    interpolatedPos =  (p * alpha) + (MixedTimeStep.prevPos * (1.0 - alpha))
    return interpolatedPos
MixedTimeStep.accumulator = 0.0
MixedTimeStep.prevPos = Position(0.0, 0.0)


