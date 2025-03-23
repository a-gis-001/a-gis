def render(*, hour, minute, filename="clock.png"):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw clock face
    clock_face = plt.Circle((0, 0), 1, color="white", ec="black", lw=3)
    ax.add_patch(clock_face)

    # Draw hour ticks
    for i in range(12):
        angle = np.pi / 6 * i
        ax.plot(
            [0.9 * np.cos(angle), np.cos(angle)],
            [0.9 * np.sin(angle), np.sin(angle)],
            color="black",
            lw=2,
        )

    # Calculate angles for hour and minute hands
    hour_angle = np.pi / 2 - (np.pi / 6 * (hour % 12 + minute / 60))
    minute_angle = np.pi / 2 - (np.pi / 30 * minute)

    # Draw hands
    ax.plot(
        [0, 0.5 * np.cos(hour_angle)],
        [0, 0.5 * np.sin(hour_angle)],
        lw=6,
        color="black",
    )
    ax.plot(
        [0, 0.8 * np.cos(minute_angle)],
        [0, 0.8 * np.sin(minute_angle)],
        lw=3,
        color="black",
    )

    # Center circle
    ax.add_patch(plt.Circle((0, 0), 0.02, color="black"))

    ax.set_aspect("equal")
    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
