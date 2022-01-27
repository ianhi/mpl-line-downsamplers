import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

from mpl_line_downsampler import ArraySource1D, DSLine2D

x = np.linspace(0, 1000, int(1e8))
largeArray = np.sin(x) + np.sin(0.5 * x) + np.sin(0.01 * x)
print("array created")

fig, ax = plt.subplots()

# don't do this
# ax.plot(largeArray)


# do this instead
down_sampler = ArraySource1D(largeArray, scale=10)

line = DSLine2D(down_sampler)
ax.add_artist(line)
ax.set_xlim([0, len(largeArray)])
ax.set_ylim(largeArray.min(), largeArray.max())
# Make a horizontal slider to control the frequency.
plt.subplots_adjust(bottom=0.25)
slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
scale_slider = Slider(
    ax=slider_ax,
    label="Downscale factor",
    valmin=10,  # don't go to 1 - slows everything down
    valmax=10000,
    valinit=10,
    valstep=1,
)
scale_slider.drawon = False  # we will draw in our update


def update_scale(scale: int):
    down_sampler.scale = scale
    fig.canvas.draw()


scale_slider.on_changed(update_scale)
plt.show()
