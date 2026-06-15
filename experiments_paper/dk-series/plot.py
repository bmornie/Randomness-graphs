import matplotlib.pyplot as plt
import numpy as np


fontsize = 16

names = ["BA", "GEO", "Ecoli", "Hpylori", "windsurfers", "coauthorship"]


dist_names = ["GCD", "NetSimile", "JDD", "RNND", "JGD", "RGDD"]
colors = ["#4477AA", "#66CCEE", "#228833", "#CCBB44", "#EE6677", "#AA3377"]
markers = ['o', 's', 'D', '*', 'P', 'd']

titles = ["BA", "GEO", "E. coli", "H. pylori", "Windsurfers", "NetScience"]


# ----- figure -----
n_rows, n_cols = 2, 3
n_curves = 6
fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 8), sharex=False, sharey=False)


handles = []

for i, ax in enumerate(axes.flat):
    distances = [np.zeros(3) for _ in range(n_curves)]
    
    with open("results/%s_results.txt" %names[i], "r") as f:
        lines = f.readlines()
    
    for n, line in enumerate(lines[1:]):
        data = line.split()
        for m in range(3):
            distances[n][m] = float(data[m+1])
    
    
    for j in range(len(distances)):
        line, = ax.plot(["0$k$", "1$k$", "2$k$"], distances[j]/distances[j][0], linewidth=2, markersize=8, marker=markers[j], label=dist_names[j], color=colors[j])

        if i == 0:  # collect handles once
            handles.append(line)

    # titles
    ax.set_title(f"{titles[i]}", fontsize=fontsize+1)

    # only left column gets y-labels
    if i % n_cols == 0:
        ax.set_ylabel("Randomness", fontsize=fontsize)

    # ticks on all axes (explicitly ensure visible)
    ax.tick_params(axis='both', which='both', labelbottom=True, labelleft=True, labelsize=fontsize)
    
    ax.set_yticks([0.0, 0.5, 1.0])
    
    

# Increase spacing between subplots
fig.subplots_adjust(
    wspace=0.25,   # horizontal spacing
    hspace=0.35,   # vertical spacing
    bottom=0.15    # space reserved for legend
)

# ----- shared legend at bottom (horizontal) -----
fig.legend(
    handles,
    dist_names,
    loc="lower center",
    ncol=n_curves,
    frameon=False,
    bbox_to_anchor=(0.5, 0.0),
    fontsize=fontsize
)


plt.savefig("dk_randomness.pdf", bbox_inches='tight')
plt.show()
