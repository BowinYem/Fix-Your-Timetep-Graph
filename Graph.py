import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.lines import Line2D 
import numpy as np
import time
import TimeStep
from TimeStep import TimeStepData
from TimeStep import SpringIntegrate

WINDOW_SIZE_X = 15
WINDOW_SIZE_Y = 10
Y_AXIS_LIM = 20
TEST_TIME = 10
INITIAL_POS = 5.0

x_points = []
y_points = []

plt.style.use('_mpl-gallery')

fig, ax = plt.subplots()
ax.set(xlim=(0, TEST_TIME), xticks=np.arange(1, TEST_TIME), 
    ylim=(-Y_AXIS_LIM, Y_AXIS_LIM), yticks=np.arange(-Y_AXIS_LIM, Y_AXIS_LIM))
fig.set_size_inches(WINDOW_SIZE_X, WINDOW_SIZE_Y, forward=True)

timeSteps = (
    TimeStepData(TimeStep.FixedTimeStep, ax.plot([], [], 'go-', lw=2)[0]),
    TimeStepData(TimeStep.VariableTimeStep, ax.plot([], [], 'ro-', lw=2)[0]),
    TimeStepData(TimeStep.SemiFixedTimeStep, ax.plot([], [], 'bo-', lw=2)[0]),
    TimeStepData(TimeStep.MixedTimeStep, ax.plot([], [], 'yo-', lw=2)[0])
)

#############################

currentPos = INITIAL_POS
start_time = time.perf_counter()
current_time = time.perf_counter()
i = 0
def Update(frame) -> list[Line2D]:
    global i, start_time, current_time, currentPos, x_points, y_points
    newTime = time.perf_counter()
    elapsedTime = newTime - start_time

    if(i >= len(timeSteps)):
        ani.pause()
    elif(elapsedTime >= TEST_TIME):
        i += 1
        start_time = newTime
        current_time = newTime
        currentPos = INITIAL_POS
        x_points = []
        y_points = []
    elif(i < len(timeSteps)):
        currentPos = timeSteps[i].function(currentPos) if (i == 0) else timeSteps[i].function(currentPos, newTime - current_time)
        current_time = newTime
        x_points.append(elapsedTime)
        y_points.append(currentPos)
        timeSteps[i].line.set_data(x_points, y_points)
        
    return [t.line for t in timeSteps]


#############################

ani = anim.FuncAnimation(fig, Update, interval=100, cache_frame_data=False, blit=True) # interval measured in ms
plt.show()
