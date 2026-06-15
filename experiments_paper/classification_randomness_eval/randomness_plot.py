import numpy as np
import matplotlib.pyplot as plt



names = ["BA", "GEO", "Ecoli", "Hpylori", "windsurfers", "coauthorship"]

GRAIP = []
SwapCon = []
GraphGen = []

i = 6
for name in names:
    with open("results/%s_rand.txt" %name, 'r') as f:
        lines = f.readlines()
    GRAIP.append(float(lines[1].split()[i]))
    SwapCon.append(float(lines[2].split()[i]))
    GraphGen.append(float(lines[3].split()[i]))

GRAIP = np.array(GRAIP)
SwapCon = np.array(SwapCon)
GraphGen = np.array(GraphGen)

# Data

# Set bar width
bar_width = 0.2
offset = 0.02

# X-axis positions
x = np.arange(len(names))

# Create bar chart
plt.figure(figsize=(12, 6))
plt.bar(x - (bar_width+offset), GRAIP, width=bar_width, label="GRAIP", color="navy", edgecolor="black", linewidth=0.6)
plt.bar(x, SwapCon, width=bar_width, label="SwapCon", color="cornflowerblue", edgecolor="black", linewidth=0.6)
plt.bar(x + (bar_width+offset), GraphGen, width=bar_width, label="GraphGen", color="lightsteelblue", edgecolor="black", linewidth=0.6)

# Add labels and title
labels = ["BA", "GEO", "E. coli", "H. pylori", "Windsurfers", "NetScience"]
plt.ylabel("Randomness", fontsize=12)
plt.xticks(ticks=x, labels=labels, fontsize=12)  # Set x-axis labels
plt.yticks(fontsize=12)
# plt.ylim((0,1.2))

# Add legend
plt.legend(fontsize=12, frameon=False)
# plt.ylim(0, 1)  # Set y-axis limit

# Show plot
plt.savefig("randomness.pdf", bbox_inches='tight')
plt.show()