# Quantifying randomness in complex graph sets using pairwise graph distances

This is the official implementation accompanying

Mornie B., Colle D., Audenaert P., Pickavet M. (2026) **Quantifying randomness in complex graph sets using pairwise graph distances**,  
submitted to Computing.

### Requirements
- Python3
- numpy
- matplotlib
- networkx
- scipy
- scikit-learn

### Installation  
**1. Clone the repository**  
```bash
git clone https://github.com/bmornie/Randomness-graphs.git
cd Randomness-graphs
```
**2. Install required dependencies**  
```bash
pip install -r requirements.txt
```

### Measuring Randomness in a set of graphs
Basic usage:
```bash
python randomness.py -i <input_folder> -d <distance>
```
This measures the Randomness, as defined in the manuscript, for the graphs stored in the input folder. Each file should contain the definition of one graph in edgelist format. See `example_input` for an example of a valid input.  
  
The following distances are implemented: "JDD", "RNND", "JGD", "RGDD", "GCD" and "NetSimile".
  
In addition, an output file can be provided with `-o <path>`. If provided, the pairwise distances between all pairs of graphs in the input folder will be written to this file. Names of input files are used to identify graphs.
  
Full example:
```bash
python randomness.py -i example_input -d JDD -o result.txt
```
This should produce the following output:
```bash
Randomness: 0.14721896062463422
Pairwise distances saved under result.txt
```

### Data and results
The folder `experiments_paper` contains all the data and code required to reproduce the experimental results in the manuscript. See the `README.md` files in each subfolder for more info. Note that running the experiments can take a long time.

### License
This project is licensed under the GNU General Public License v3.0.  
See the `LICENSE` file for details.
