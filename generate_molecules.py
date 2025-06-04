import argparse
import itertools
import os
import selfies
from rdkit import Chem
from rdkit.Chem import Draw


def main():
    parser = argparse.ArgumentParser(
        description="Generate all unique combinations of SELFIES tokens, convert to SMILES, and plot with RDKit"
    )
    parser.add_argument(
        "tokens",
        nargs="+",
        help="List of SELFIES tokens, e.g. '[C] [O]'"
    )
    parser.add_argument(
        "--output-dir",
        default="molecule_plots",
        help="Directory where molecule images will be saved"
    )
    args = parser.parse_args()

    tokens = args.tokens
    # Generate unique permutations using each token once
    perms = set(itertools.permutations(tokens))
    print(f"Total combinations: {len(perms)}")

    # Convert permutations to canonical SMILES and de-duplicate
    unique = {}
    for perm in perms:
        selfie = "".join(perm)
        try:
            smiles = selfies.decoder(selfie)
        except Exception as e:
            print(f"Failed to decode SELFIES {selfie}: {e}")
            continue
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"Failed to create molecule from SMILES {smiles}")
            continue
        canonical = Chem.MolToSmiles(mol, canonical=True)
        if canonical not in unique:
            unique[canonical] = (selfie, mol)
        else:
            print(f"Duplicate SMILES {canonical} encountered; skipping")

    print(f"Unique molecules: {len(unique)}")

    os.makedirs(args.output_dir, exist_ok=True)

    for i, (smiles, (selfie, mol)) in enumerate(unique.items(), 1):
        img = Draw.MolToImage(mol)
        img_path = os.path.join(args.output_dir, f"molecule_{i}.png")
        img.save(img_path)
        print(f"{selfie} -> {smiles} saved to {img_path}")


if __name__ == "__main__":
    main()
