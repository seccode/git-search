Git Searcher is a command line utility to search git commits for either an added or removed string. It is helpful for determining where code originated from.

# Example usage
```
python search.py --repo=MyRepo --added="import argparse, os, subprocess"
```

```
python search.py --repo=MyRepo --removed="from tqdm import tqdm"
```
