#!/usr/bin/env python3
"""linecount - Fast line/word/byte counter (wc alternative)."""
import os, argparse, sys

def count_file(path):
    lines = words = chars = 0
    try:
        with open(path, 'rb') as f:
            for line in f:
                lines += 1
                chars += len(line)
                words += len(line.split())
    except (OSError, IOError) as e:
        return None
    return {'lines': lines, 'words': words, 'bytes': chars, 'file': path}

def fmt(n):
    return f"{n:>8,}"

def main():
    p = argparse.ArgumentParser(description='Line/word/byte counter')
    p.add_argument('files', nargs='*', help='Files (stdin if omitted)')
    p.add_argument('-l', '--lines', action='store_true', help='Lines only')
    p.add_argument('-w', '--words', action='store_true', help='Words only')
    p.add_argument('-c', '--bytes', action='store_true', help='Bytes only')
    p.add_argument('-r', '--recursive', action='store_true')
    p.add_argument('-e', '--ext', nargs='*', help='File extensions filter')
    args = p.parse_args()

    show_all = not (args.lines or args.words or args.bytes)
    files = []

    if not args.files:
        data = sys.stdin.buffer.read()
        lines = data.count(b'\n')
        words = len(data.split())
        result = {'lines': lines, 'words': words, 'bytes': len(data), 'file': '(stdin)'}
        if show_all: print(f"{fmt(lines)} {fmt(words)} {fmt(len(data))}")
        elif args.lines: print(lines)
        elif args.words: print(words)
        elif args.bytes: print(len(data))
        return

    for f in args.files:
        if os.path.isdir(f) and args.recursive:
            for root, dirs, fnames in os.walk(f):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for fn in fnames:
                    if args.ext and not any(fn.endswith(f'.{e}') for e in args.ext): continue
                    files.append(os.path.join(root, fn))
        else:
            files.append(f)

    totals = {'lines': 0, 'words': 0, 'bytes': 0}
    for path in files:
        result = count_file(path)
        if not result: continue
        for k in totals: totals[k] += result[k]
        if show_all:
            print(f"{fmt(result['lines'])} {fmt(result['words'])} {fmt(result['bytes'])}  {path}")
        elif args.lines: print(f"{fmt(result['lines'])}  {path}")
        elif args.words: print(f"{fmt(result['words'])}  {path}")
        elif args.bytes: print(f"{fmt(result['bytes'])}  {path}")

    if len(files) > 1:
        if show_all:
            print(f"{fmt(totals['lines'])} {fmt(totals['words'])} {fmt(totals['bytes'])}  total")
        elif args.lines: print(f"{fmt(totals['lines'])}  total")

if __name__ == '__main__':
    main()
