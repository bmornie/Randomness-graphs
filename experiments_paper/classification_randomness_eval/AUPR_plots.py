import numpy as np
import matplotlib.pyplot as plt


fontsize = 12

names = ["BA", "GEO", "Ecoli", "Hpylori", "windsurfers", "coauthorship"]


dist_names = ["GCD", "NetSimile", "JDD", "RNND", "JGD", "RGDD"]
colors = ["#4477AA", "#66CCEE", "#228833", "#CCBB44", "#EE6677", "#AA3377"]
linestyles = ['solid']*6

titles = ["BA", "GEO", "E. coli", "H. pylori", "Windsurfers", "NetScience"]


# ----- figure -----
n_rows, n_cols = 2, 3
n_curves = 6
fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 8), sharex=False, sharey=False)


handles = []

for i, ax in enumerate(axes.flat):
    with np.load(f"results/{names[i]}_AUPR.npz") as npzfile:
        for j, distance in enumerate(["GCD11", "NetSimile", "JDM", "RNN", "JGM", "RGD"]):
            precision = npzfile["%s_precision" %distance]
            recall = npzfile["%s_recall" %distance]
            
            if i == 0 and distance == "JGM":
                precision = np.delete(precision, -2)
                recall = np.delete(recall, -2)
                precision = np.delete(precision, -2)
                recall = np.delete(recall, -2)
                precision = np.delete(precision, -2)
                recall = np.delete(recall, -2)
            
            line, = ax.plot(recall, precision, label=dist_names[j], color=colors[j], linestyle=linestyles[j], linewidth=2)
            
            if i == 0:  # collect handles once
                handles.append(line)
    
    # --- square axes ---
    ax.set_box_aspect(1)

    # --- fixed limits ---
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # titles
    ax.set_title(f"{titles[i]}", fontsize=fontsize+1)
    
    # only bottom row gets x-labels
    if i // n_cols == n_rows - 1:
        ax.set_xlabel("Recall", fontsize=fontsize)

    # only left column gets y-labels
    if i % n_cols == 0:
        ax.set_ylabel("Precision", fontsize=fontsize)

    # ticks on all axes (explicitly ensure visible)
    ax.tick_params(axis='both', which='both', labelbottom=True, labelleft=True, labelsize=fontsize)
    
    

# Increase spacing between subplots
fig.subplots_adjust(
    wspace=0.25,   # horizontal spacing
    hspace=0.25,   # vertical spacing
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


plt.savefig("PR_curves.pdf", bbox_inches='tight')
plt.show()




#%%

names = ["BA", "GEO", "Ecoli", "Hpylori", "windsurfers", "coauthorship"]
dist_names = ["GCD", "NetSimile", "JDD", "RNND", "JGD", "RGDD"]
colors = ["#4477AA", "#66CCEE", "#228833", "#CCBB44", "#EE6677", "#AA3377"]

GCD = []
NetSimile = []
JDD = []
RNND = []
JGD = []
RGDD = []

for name in names:
    with np.load("results/%s_AUPR.npz" %name) as npzfile:
        GCD.append(npzfile["GCD11_aupr"])
        NetSimile.append(npzfile["NetSimile_aupr"])
        JDD.append(npzfile["JDM_aupr"])
        RNND.append(npzfile["RNN_aupr"])
        JGD.append(npzfile["JGM_aupr"])
        RGDD.append(npzfile["RGD_aupr"])


# Data

# Set bar width
bar_width = 0.13
offset = 0.01

# X-axis positions
x = np.arange(len(names))

# Create bar chart
plt.figure(figsize=(12, 6))
plt.bar(x - 5*(bar_width+offset)/2, GCD, width=bar_width, label="GCD", color="#4477AA")
plt.bar(x - 3*(bar_width+offset)/2, NetSimile, width=bar_width, label="NetSimile", color="#66CCEE")
plt.bar(x - (bar_width+offset)/2, JDD, width=bar_width, label="JDD", color="#228833")
plt.bar(x + (bar_width+offset)/2, RNND, width=bar_width, label="RNND", color="#CCBB44")
plt.bar(x + 3*(bar_width+offset)/2, JGD, width=bar_width, label="JGD", color="#EE6677")
plt.bar(x + 5*(bar_width+offset)/2, RGDD, width=bar_width, label="RGDD", color="#AA3377")

# Add labels and title
labels = ["BA", "GEO", "E. coli", "H. pylori", "Windsurfers", "NetScience"]
plt.ylabel("AUPR", fontsize=12)
plt.xticks(ticks=x, labels=labels, fontsize=12)  # Set x-axis labels
plt.yticks(fontsize=12)


# Add legend
plt.legend(fontsize=12)
plt.ylim(0, 1)  # Set y-axis limit

# Show plot
plt.savefig("AUPR.pdf", bbox_inches='tight')
plt.show()