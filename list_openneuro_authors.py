"""Get demographic data from openneuro datasets."""

import json
import re
from pathlib import Path

from rich import print

openneuro_super_ds = Path("/home/remi/datalad/datasets.datalad.org/openneuro")

AUTHORS_TO_IGNORE = ["TODO:"]


def list_authors(ds_desc: dict):
    """List authors from dataset description."""
    authors = ds_desc.get("Authors")

    if authors is None:
        return None

    sanitized_authors = []

    if len(authors) == 1:
        authors = authors[0]
    if isinstance(authors, str):
        authors = authors.split("., ")

    for author_ in authors:
        if author_ in AUTHORS_TO_IGNORE:
            continue
        author_ = re.sub(r"\(.*\)", "", author_)
        author_ = author_.replace(",", "")
        author_ = author_.replace(".", "")
        sanitized_authors.append(author_.lower())

    return sanitized_authors


def main():
    """Get demographic data from openneuro datasets."""
    datasets = [
        d
        for d in openneuro_super_ds.iterdir()
        if (d.is_dir() and d.stem not in [".git"])
    ]

    authors = []
    ethics = []

    for ds in datasets:
        if not (ds / "dataset_description.json").exists():
            continue

        with open(ds / "dataset_description.json") as f:
            ds_desc = json.load(f)

        new_authors = list_authors(ds_desc)
        if new_authors is not None:
            authors.extend(new_authors)

        if ds_desc.get("EthicsApprovals") not in (None, ""):
            ethics.extend(ds_desc.get("EthicsApprovals"))

    authors = sorted(set(authors))

    print(authors)
    print(f"nb authors found: {len(authors)}")

    ethics = sorted(set(ethics))
    print(ethics)
    print(len(ethics))


if __name__ == "__main__":
    main()
