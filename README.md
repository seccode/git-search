Git Searcher is a command line utility to search git commits for either an added or removed string. It is helpful for determining where code originated from.

# Example usage
```
python search.py --repo=path/to/repo --added="import argparse, os, subprocess"
```

```
python search.py --repo=path/to/repo --removed="from tqdm import tqdm"
```
