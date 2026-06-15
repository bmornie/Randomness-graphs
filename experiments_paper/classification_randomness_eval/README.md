Python script `AUPR.py` can be used to compute Precision-Recall curves and AUPR values based on the graphs stored in `graphs.zip` (extract first).  
The files produced by this script are quite large, and therefore not included in this repository. The exact data used for the figures in the paper can be requested from the corresponding author.  

Fig. 4 and Fig. 5 in the manuscript can be reproduced by running `AUPR_plots.py`, provided you have obtained the AUPR data for each source network.  
  
Randomness of generated graphs is stored in `results`. This data can be reproduced with `randomness_analysis.py`.  
Fig. 6 in the manuscript can be reproduced by running `randomness_plot.py`.  

The graphs have been generated using [GRAIP](https://github.com/bmornie/GRAIP) and [GraphGen](https://github.com/idea-iitd/graphgen), both available on GitHub.
