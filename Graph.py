import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time
import TimeStep
from TimeStep import TimeStepData
from Pos import Position

WINDOW_SIZE_X = 15
WINDOW_SIZE_Y = 10
X_AXIS_LIM = 20
Y_AXIS_LIM = 20
TEST_TIME = 10

timeSteps = (
    TimeStepData(TimeStep.FixedTimeStep, 'green', 'o'),
    TimeStepData(TimeStep.VariableTimeStep, 'red', '+'),
    TimeStepData(TimeStep.SemiFixedTimeStep, 'blue', '*'),
    TimeStepData(TimeStep.MixedTimeStep, 'yellow', '^')
)

currentPos = Position(0.0, 0.0)
start_time = time.perf_counter()
current_time = time.perf_counter()
i = 0
def Update(frame, *fargs) -> None:
    global i, start_time, current_time, currentPos
    newTime = time.perf_counter()
    elapsedTime = newTime - start_time

    if(i >= len(timeSteps)):
        ani.pause()
    elif(elapsedTime >= TEST_TIME):
        i += 1
        start_time = newTime
        current_time = newTime
        currentPos = Position(0.0, 0.0)
    elif(i < len(timeSteps)):
        newPos = timeSteps[i].function(currentPos) if (i == 0) else timeSteps[i].function(currentPos, newTime - current_time)
        current_time = newTime
        ax.plot(elapsedTime, newPos.y, timeSteps[i].marker, linewidth=2.0, color = timeSteps[i].color)

####################

plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.set(xlim=(0, X_AXIS_LIM), xticks=np.arange(1, X_AXIS_LIM), 
    ylim=(0, Y_AXIS_LIM), yticks=np.arange(1, Y_AXIS_LIM))
fig.set_size_inches(WINDOW_SIZE_X, WINDOW_SIZE_Y, forward=True)

ani = anim.FuncAnimation(fig, Update, interval=100, cache_frame_data=False) # interval measured in ms
plt.show()
