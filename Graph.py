import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.artist import Artist 
from matplotlib.text import Text
import numpy as np
import time
import TimeStep
from TimeStep import TimeStepData
import integratefunc
from integratefunc import IntegrateEnum

X_LABEL = "Time Elapsed"
Y_LABEL = "Position"
TITLE = "Spring Damping" 
WINDOW_SIZE_X = 15
WINDOW_SIZE_Y = 10
Y_AXIS_LIM = 20
TEST_TIME = 10
INITIAL_POS = 5.0
INTEGRATE = IntegrateEnum.SPRING_INTG
RESULT_TEXT_X = .05
RESULT_TEXT_Y = Y_AXIS_LIM - 4.8
RESULT_TEXT_LINESPC = 1.5
RESULT_TEXT_BGCOLOR = "grey"
TOTAL_TESTS = 5

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

def UpdatePosText(t : Text):
    positionText = "Final Positions:\n"
    for ts in timeSteps:
        positionText += "   " + ts.name + ": " + ", ".join(str(round(pos,2)) for pos in ts.finalPos) + '\n'
    t = plt.text(RESULT_TEXT_X, RESULT_TEXT_Y, positionText, backgroundcolor=RESULT_TEXT_BGCOLOR, linespacing=RESULT_TEXT_LINESPC)
    return t

resultText = plt.text(RESULT_TEXT_X, RESULT_TEXT_Y, "", backgroundcolor=RESULT_TEXT_BGCOLOR, linespacing=RESULT_TEXT_LINESPC)
resultText = UpdatePosText(resultText)

plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
plt.title(TITLE)
plt.tight_layout()

#############################

currentPos = INITIAL_POS
start_time = time.perf_counter()
current_time = time.perf_counter()
currentTest = 0
i = 0
def Update(frame) -> list[Artist]:
    global i, currentTest, start_time, current_time, currentPos, x_points, y_points, resultText
    newTime = time.perf_counter()
    elapsedTime = newTime - start_time

    if(currentTest >= TOTAL_TESTS):
        ani.pause()
    elif(i >= len(timeSteps)):
        i = 0
        currentTest += 1
        for ts in timeSteps:
            ts.line.set_data(x_points, y_points) 
    elif(elapsedTime >= TEST_TIME):
        start_time = newTime
        current_time = newTime
        timeSteps[i].finalPos.append(currentPos)
        currentPos = INITIAL_POS
        x_points = []
        y_points = []
        integratefunc.velocity = 0
        resultText = UpdatePosText(resultText)
        i += 1
    elif(i < len(timeSteps)):
        currentPos =  timeSteps[i].function(currentPos, INTEGRATE, newTime - current_time)
        current_time = newTime
        x_points.append(elapsedTime)
        y_points.append(currentPos)
        timeSteps[i].line.set_data(x_points, y_points)
        
    returnArtist : list[Artist] = [t.line for t in timeSteps]
    returnArtist.append(resultText)
    return returnArtist

#############################

ani = anim.FuncAnimation(fig, Update, interval=100, cache_frame_data=False, blit=True) # interval measured in ms
plt.show()

"""
To do:
- Add Labels (A key, axis labels)
- Text for our final position(s) 
- Repeat test option
"""