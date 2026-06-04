#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'data/processed/journal_v1/main_all_traces.jsonl'
OUT = ROOT / 'results/reports/journal_v1/main_h6_semantic_consistency_audit.md'

NEG_IRREV_MARKERS = ['no successful correction', 'persisted', 'insufficient to neutralize', 'unrecovered']
POS_IRREV_MARKERS = ['successfully corrected', 'recovered', 'neutralized']
DOWNSTREAM_MARKERS = ['downstream ', ' reused', 'integrated', 'consumed', 'inherits faulty']
TEXTUAL_ONLY_MARKERS = ['repeated wording', 'textual repetition only']


def main():
    rows=[json.loads(x) for x in CORPUS.read_text(encoding='utf-8').splitlines() if x.strip()]
    issues=[]
    cats={
        'irrev_false_but_persistent':0,
        'irrev_true_but_recovered':0,
        'recover_false_but_available':0,
        'recover_true_but_unavailable':0,
        'prop_true_but_textual_only':0,
        'prop_false_but_downstream':0,
        'generic_rationale':0,
    }
    for r in rows:
        tid=r['trace_id']
        irrev=str(r.get('irreversibility_evidence','')).lower()
        prop=str(r.get('propagation_evidence','')).lower()
        ropp=str(r.get('recovery_opportunity','')).lower()
        rationale=str(r.get('label_rationale','')).lower()
        if r.get('gold_irreversibility') is False and any(m in irrev for m in NEG_IRREV_MARKERS):
            cats['irrev_false_but_persistent']+=1;issues.append((tid,'irrev_false_but_persistent'))
        if r.get('gold_irreversibility') is True and any(m in irrev for m in POS_IRREV_MARKERS):
            cats['irrev_true_but_recovered']+=1;issues.append((tid,'irrev_true_but_recovered'))
        if r.get('gold_recoverability') is False and ropp in {'available_and_used','available_but_missed'}:
            cats['recover_false_but_available']+=1;issues.append((tid,'recover_false_but_available'))
        if r.get('gold_recoverability') is True and ropp in {'not_applicable_or_unavailable','none',''}:
            cats['recover_true_but_unavailable']+=1;issues.append((tid,'recover_true_but_unavailable'))
        if r.get('gold_propagation') is True and any(m in prop for m in TEXTUAL_ONLY_MARKERS):
            cats['prop_true_but_textual_only']+=1;issues.append((tid,'prop_true_but_textual_only'))
        if r.get('gold_propagation') is False and any(m in prop for m in DOWNSTREAM_MARKERS):
            cats['prop_false_but_downstream']+=1;issues.append((tid,'prop_false_but_downstream'))
        if rationale in {
            'stored as non-model-visible metadata with explicit dependency/recovery evidence',
            'generic rationale',
        }:
            cats['generic_rationale']+=1;issues.append((tid,'generic_rationale'))
    total=sum(cats.values())
    lines=['# Main H6 Semantic Consistency Audit','',f'- total_traces: {len(rows)}',f'- total_inconsistencies: {total}','', '| category | count |','|---|---:|']
    for k,v in cats.items(): lines.append(f'| {k} | {v} |')
    lines += ['','## Sample issues (first 30)','']+[f'- {t}: {c}' for t,c in issues[:30]]
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'H6 inconsistencies: {total}')
    print('FINAL:', 'PASS' if total==0 else 'FAIL')
    return 0 if total==0 else 1

if __name__=='__main__':
    raise SystemExit(main())
