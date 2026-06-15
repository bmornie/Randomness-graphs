import numpy as np
import matplotlib.pyplot as plt



with np.load("WS_data.npz") as npzfile:
    C = npzfile['C']
    L = npzfile['L']
    GCD11 = npzfile['GCD11']
    NetSimile = npzfile['NetSimile']
    JDD = npzfile['JDD']
    RNND = npzfile['RNND']
    JGD = npzfile['JGD']
    RGDD = npzfile['RGDD']

prob = np.logspace(-4, 0, 20)
# plt.figure(figsize=(5,4))
plt.plot(prob, C/max(C), marker='^', linewidth=0.5, markersize=3, label="$1 - C(p)/C(0)$", color="black")
plt.plot(prob, L/max(L), marker='v', linewidth=0.5, markersize=3, label="$1 - L(p)/L(0)$", color='gray')
plt.plot(prob, GCD11/max(GCD11), marker='o', linewidth=0.5, markersize=3, label="GCD", color="#4477AA")
plt.plot(prob, NetSimile/max(NetSimile), marker='s', linewidth=0.5, markersize=3, label="NetSimile", color="#66CCEE")
plt.plot(prob, JDD/max(JDD), marker='D', linewidth=0.5, markersize=3, label="JDD", color="#228833")
plt.plot(prob, RNND/max(RNND), marker='*', linewidth=0.5, markersize=3, label="RNND", color="#CCBB44")
plt.plot(prob, JGD/max(JGD), marker='P', linewidth=0.5, markersize=3, label="JGD", color="#EE6677")
plt.plot(prob, RGDD/max(RGDD), marker='d', linewidth=0.5, markersize=3, label="RGDD", color="#AA3377")
plt.xscale("log")
plt.xlabel("$p$")
plt.ylabel("distance")
plt.gca().tick_params(axis='both', which='both', direction='in', top=True, right=True)
plt.legend()
plt.legend().set_visible(False)
plt.savefig("WS.pdf", bbox_inches='tight')
plt.show()