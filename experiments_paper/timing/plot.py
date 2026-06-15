import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator


fontsize = 16
results_dir = "results"

distances = ["JDD", "RNND", "JGD", "RGDD"]

# Left plot: varying n, fixed m = 5n
n_values_left = [100, 200, 400, 800, 1600]

# Right plot: fixed n=200, varying m = d*n
n_fixed = 200
d_values = [2, 4, 8, 16]


# ----------------------------
# HELPERS
# ----------------------------
def load_stats(distance, n, m):
    """Load file and return mean and std of 100 runs."""
    path = f"{results_dir}/timing_{distance}_{n}_{m}.txt"
    data = np.loadtxt(path)
    return np.mean(data), np.std(data)


def collect_left():
    """Returns dict: distance -> (x, mean, std) for varying n."""
    results = {}
    for dist in distances:
        means, stds = [], []
        for n in n_values_left:
            m = 5 * n
            mean, std = load_stats(dist, n, m)
            means.append(mean)
            stds.append(std)
        results[dist] = (np.array(n_values_left), np.array(means), np.array(stds))
    return results


def collect_right():
    """Returns dict: distance -> (x, mean, std) for varying d."""
    results = {}
    for dist in distances:
        means, stds = [], []
        x_vals = []
        for d in d_values:
            n = n_fixed
            m = d * n
            mean, std = load_stats(dist, n, m)
            x_vals.append(d)
            means.append(mean)
            stds.append(std)
        results[dist] = (np.array(x_vals), np.array(means), np.array(stds))
    return results


# ----------------------------
# LOAD DATA
# ----------------------------
left_data = collect_left()
right_data = collect_right()


# ----------------------------
# PLOTTING
# ----------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors = ["#228833", "#CCBB44", "#EE6677", "#AA3377"]
markers = ["D", "*", "P", "d"]

# ---- LEFT: scaling with n ----
ax = axes[0]
for i, dist in enumerate(distances):
    x, mean, std = left_data[dist]
    ax.errorbar(x, mean, yerr=std, marker=markers[i], capsize=4, label=dist, color=colors[i])

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xticks(n_values_left)
ax.set_xticklabels(n_values_left, fontsize=fontsize)
ax.set_xlabel("Number of nodes", fontsize=fontsize)
ax.set_ylabel("Running time (s)", fontsize=fontsize)


# ---- RIGHT: scaling with density ----
ax = axes[1]
for i, dist in enumerate(distances):
    x, mean, std = right_data[dist]
    ax.errorbar(x, mean, yerr=std, marker=markers[i], capsize=4, label=dist, color=colors[i])

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xticks(d_values)
ax.set_xticklabels(d_values, fontsize=fontsize)
ax.xaxis.set_minor_locator(NullLocator())
ax.set_xlabel("Edges per node", fontsize=fontsize)


for ax in axes:
    ax.set_ylim(2e-4, 5)
    ax.xaxis.set_minor_locator(NullLocator())
    ax.tick_params(axis='both', labelsize=fontsize)
    ax.grid(axis='y', which='major', linestyle='dashed', linewidth=1, alpha=0.7)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1)


fig.text(0.01, 0.98, "(a)", fontsize=fontsize, fontweight="bold", va="top", ha="left")
fig.text(0.51, 0.98, "(b)", fontsize=fontsize, fontweight="bold", va="top", ha="left")


# Collect handles + labels from one of the axes (they are identical across both)
handles, labels = axes[0].get_legend_handles_labels()

# Place a single legend below the figure
fig.legend(
    handles, labels,
    loc="lower center",
    ncol=len(labels),   # puts items side-by-side
    fontsize=fontsize,
    frameon=False
)

# Make room at the bottom for the legend
plt.tight_layout(rect=[0, 0.12, 1, 1])

plt.savefig("timing.pdf", bbox_inches="tight")
plt.show()