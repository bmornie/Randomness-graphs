Computation times for the proposed distances can be determined using `timing.py`.  

Usage:
```bash
python timing.py <distance> <nodes> <edges_per_node> <runs>
```
This generates `<runs>` pairs of ER graphs of the provided size, computes the distance between each pair using `<distance>`, and stores the computation times (in seconds) in `timing_<distance>_<nodes>_<edges>.txt`.  
`<distance>` can be `JDD`, `RNND`, `JGD` or `RGDD`.

The data used in the manuscript is stored in `results`. Fig. 7 can be reproduced by running `plot.py`.  
  
Please note that computation times can depend heavily on the hardware.
