# GraphGen - MWCP Instance Generator

A Python tool for generating random graph instances for the Maximum Weight Clique Problem (MWCP) with exact solutions.

## Description

This tool generates random graphs using the Erdos-Renyi model (G(n,p)), assigns random weights to nodes, and computes the exact maximum weight clique solution using NetworkX. The generated instances are exported in a modified DIMACS format suitable for C++/Java programs.

## Requirements

- Python 3.6 or higher
- NetworkX >= 3.0
- Matplotlib >= 3.5.0

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Randinh0/Graphgen.git
cd Graphgen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a graph instance with default parameters (100 nodes, 0.5 edge probability):
```bash
python generar_instancia_mwcp.py
```

### Command Line Options

- `-n, --nodos`: Number of nodes in the graph (default: 100)
- `-p, --probabilidad`: Edge probability between two nodes, range 0-1 (default: 0.5)
- `-s, --semilla`: Random seed for reproducibility (default: 42)
- `-o, --output`: Output file for the graph in DIMACS format (default: test_instance.txt)
- `--solucion`: Output file for the optimal solution (default: solucion.txt)
- `--no-export`: Do not export files, only display results

### Examples

Generate a graph with 50 nodes and 0.3 edge probability:
```bash
python generar_instancia_mwcp.py -n 50 -p 0.3
```

Generate a graph with custom output files:
```bash
python generar_instancia_mwcp.py -n 200 -p 0.4 -o my_graph.txt --solucion my_solution.txt
```

Generate with a specific seed for reproducibility:
```bash
python generar_instancia_mwcp.py -n 100 -p 0.5 -s 123
```

Display results without exporting files:
```bash
python generar_instancia_mwcp.py -n 50 --no-export
```

## Output Format

### Graph File (DIMACS format)

The graph is exported in a modified DIMACS format:
- First line: number of nodes and edges
- Lines starting with 'n': node definition with weight (1-based indexing)
- Lines starting with 'e': edge definition (1-based indexing)

Example:
```
100 2450
n 1 150
n 2 87
...
e 1 2
e 1 3
...
```

### Solution File

The solution file contains:
- Total weight of the optimal clique
- Number of nodes in the clique
- List of nodes in the clique
- Individual weights of each node in the clique

## Notes

- For large graphs, computing the exact solution may take significant time
- Node weights are randomly assigned in the range 1-200
- The algorithm uses NetworkX's max_weight_clique function, which implements variants of the Ostergard or Carraghan-Pardalos algorithms

