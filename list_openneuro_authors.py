"""Get demographic data from openneuro datasets."""

import json
import re
from pathlib import Path

from rich import print

openneuro_super_ds = Path("/home/remi/datalad/datasets.datalad.org/openneuro")

def main():

    datasets = [
        d for d in openneuro_super_ds.iterdir() if (d.is_dir() and d.stem not in [".git"])
    ]

    authors = []

    for ds in datasets:

        if not (ds / "dataset_description.json").exists():
            continue

        with open(ds / "dataset_description.json") as f:
            ds_desc = json.load(f)


        new_authors = ds_desc.get("Authors")

        if new_authors is None:
            continue

        # sanitize authors
        if len(new_authors) == 1:
            new_authors = new_authors[0]
        if isinstance(new_authors, str):
            new_authors = new_authors.split("., ")  
        
        for author_ in new_authors:
            if author_ in ["TODO:"]:
                continue
            author_ = re.sub(r"\(.*\)", "", author_)
            author_ = author_.replace(",", "")
            author_ = author_.replace(".", "")
            authors.append(author_.lower())

        


    authors = sorted(set(authors))
    print(authors)

    print(len(authors))