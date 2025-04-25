import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Field dimensions (in meters)
FIELD_LENGTH = 105
FIELD_WIDTH = 68

def draw_pitch(ax):
    # Pitch outline & center line
    ax.add_patch(patches.Rectangle((0, 0), FIELD_LENGTH, FIELD_WIDTH, fill=False, linewidth=2))
    ax.plot([FIELD_LENGTH / 2, FIELD_LENGTH / 2], [0, FIELD_WIDTH], color='black')

    # Penalty areas
    ax.add_patch(patches.Rectangle((0, (FIELD_WIDTH - 40.32)/2), 16.5, 40.32, fill=False))
    ax.add_patch(patches.Rectangle((FIELD_LENGTH - 16.5, (FIELD_WIDTH - 40.32)/2), 16.5, 40.32, fill=False))

    # Goal boxes
    ax.add_patch(patches.Rectangle((0, (FIELD_WIDTH - 18.32)/2), 5.5, 18.32, fill=False))
    ax.add_patch(patches.Rectangle((FIELD_LENGTH - 5.5, (FIELD_WIDTH - 18.32)/2), 5.5, 18.32, fill=False))

    # Center circle and penalty spots
    center_circle = plt.Circle((FIELD_LENGTH / 2, FIELD_WIDTH / 2), 9.15, color='black', fill=False)
    ax.add_patch(center_circle)
    ax.plot([11], [FIELD_WIDTH/2], marker='o', markersize=3, color="black")
    ax.plot([FIELD_LENGTH - 11], [FIELD_WIDTH/2], marker='o', markersize=3, color="black")

    # Corner arcs
    corners = [(0, 0), (0, FIELD_WIDTH), (FIELD_LENGTH, 0), (FIELD_LENGTH, FIELD_WIDTH)]
    for x, y in corners:
        corner_arc = patches.Arc((x, y), 2, 2, angle=0, theta1=0, theta2=90, color='black')
        if x == 0 and y == 0:
            ax.add_patch(corner_arc)
        elif x == 0 and y == FIELD_WIDTH:
            ax.add_patch(patches.Arc((x, y), 2, 2, angle=0, theta1=270, theta2=360, color='black'))
        elif x == FIELD_LENGTH and y == 0:
            ax.add_patch(patches.Arc((x, y), 2, 2, angle=0, theta1=90, theta2=180, color='black'))
        else:
            ax.add_patch(patches.Arc((x, y), 2, 2, angle=0, theta1=180, theta2=270, color='black'))

    ax.set_xlim(0, FIELD_LENGTH)
    ax.set_ylim(0, FIELD_WIDTH)
    ax.set_aspect('equal')
    ax.set_title("Hover over the pitch to see coordinates (in meters)")

def on_mouse_move(event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        text.set_text(f"x: {x:.2f} m, y: {y:.2f} m")
        fig.canvas.draw_idle()

fig, ax = plt.subplots(figsize=(12, 7))
draw_pitch(ax)

text = ax.text(0.02, 1.02, '', transform=ax.transAxes, fontsize=12)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

plt.show()
