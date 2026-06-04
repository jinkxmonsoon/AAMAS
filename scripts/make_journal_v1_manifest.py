#!/usr/bin/env python3
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/artifact_manifests/journal_v1_main_corpus_manifest.md'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: Path) -> int:
    return sum(1 for _ in path.open('r', encoding='utf-8'))


def categorize(path: Path) -> str:
    s = str(path)
    if 'data/processed/journal_v1' in s:
        return 'main_corpus_data'
    if 'results/reports/journal_v1' in s:
        return 'main_corpus_report'
    return 'other'


def main():
    targets = [
        ROOT / 'data/processed/journal_v1/main_clean_traces.jsonl',
        ROOT / 'data/processed/journal_v1/main_perturbed_traces.jsonl',
        ROOT / 'data/processed/journal_v1/main_all_traces.jsonl',
    ]
    targets.extend(sorted((ROOT / 'results/reports/journal_v1').glob('*.md')))

    lines = [
        '# Journal-v1 Main Corpus Artifact Manifest',
        '',
        '- Artifact freeze scope: Journal-v1 main controlled corpus and its audit/diagnostic reports.',
        '- Method-performance outputs: none.',
        '',
        '| artifact_path | category | bytes | lines | sha256 |',
        '|---|---:|---:|---:|---|',
    ]

    for p in targets:
        rel = p.relative_to(ROOT)
        lines.append(f'| `{rel}` | {categorize(p)} | {p.stat().st_size} | {line_count(p)} | `{sha256(p)}` |')

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'WROTE {OUT.relative_to(ROOT)} with {len(targets)} entries')


if __name__ == '__main__':
    main()
