Git Searcher is a command line utility to search git commits for either an added or removed string. It is helpful for determining where code originated from.

# Example usage
```
python search.py --repo=path/to/repo --added="import argparse, os, subprocess"
```

```
python search.py --repo=path/to/repo --removed="from tqdm import tqdm"
```

The expected output from this tool is:
```
<SEARCH_STRING> [added/removed] in Commit: <COMMIT_ID>, File: <FILENAME>, Line: <LINE_NUMBER>
```
The tool can find multiple instances of the search string found
