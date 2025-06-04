# New_molecules

Creating new molecules from selfies tokens.

## Usage

Install the required libraries:

```bash
pip install selfies rdkit
```

Run the generator with a list of SELFIES tokens. Each token will appear once
in every generated permutation and duplicate permutations are removed. The
resulting SMILES strings are canonicalized with RDKit so that identical
molecules are skipped.

```bash
python generate_molecules.py '[C]' '[C]' '[C]' '[O]' '[O]'
```

Resulting molecule images are written to the `molecule_plots` directory.
