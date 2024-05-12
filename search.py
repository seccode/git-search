import argparse, os, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def search_in_commit(commit_id, added, removed):
    file_name, line_number, results = None, None, []
    try:
        diff_lines = subprocess.check_output(['git', 'diff', '--ignore-all-space', '--unified=0', commit_id + '^', commit_id], stderr=subprocess.STDOUT).decode('utf-8', 'ignore').split("\n")
    except subprocess.CalledProcessError: # Intiial commit
        diff_lines = subprocess.check_output(['git', 'show', '--format=', '--unified=0', commit_id], stderr=subprocess.STDOUT).decode('utf-8', 'ignore').split("\n")
    for line in diff_lines:
        if line.startswith('diff --git'):
            file_name = line.split(' b/')[-1]
            line_number = None
        elif line.startswith('@@'):
            line_number = int(line.split(' ')[2].split(',')[0][1:])
        elif line.startswith('+'):
            if added and added in line:
                results.append(f"'{added}' added in Commit: {commit_id}, File: {file_name}, Line: {line_number}")
            if line_number:
                line_number += 1
        elif line.startswith('-'):
            if removed and removed in line:
                results.append(f"'{removed}' removed in Commit: {commit_id}, File: {file_name}, Line: {line_number}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Search Git commits for a specific string")
    parser.add_argument("--repo", type=str, help="Path to the repository")
    parser.add_argument("--added", type=str, help="Added string to search for")
    parser.add_argument("--removed", type=str, help="Removed string to search for")
    args = parser.parse_args()
    assert args.repo, "Must specify a --repo"
    assert args.added or args.removed, "Must specify an --added or --removed string"
    os.chdir(args.repo)
    subprocess.run(['git', 'fetch', '--all'], check=True)
    commit_ids = subprocess.check_output(['git', 'rev-list', '--all']).decode('utf-8').splitlines()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for future in tqdm(as_completed({executor.submit(search_in_commit, commit_id, args.added, args.removed): commit_id for commit_id in commit_ids}), total=len(commit_ids)):
            results = future.result()
            if results:
                for result in results:
                    print(result)

if __name__ == "__main__":
    main()
