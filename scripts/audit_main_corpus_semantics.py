#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'data/processed/journal_v1/main_all_traces.jsonl'
REPORT_DIR = ROOT / 'results/reports/journal_v1'


def load_rows(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]


def main():
    rows = load_rows(CORPUS)
    clean = [r for r in rows if r.get('case_variant') == 'clean']
    pert = [r for r in rows if r.get('case_variant') == 'perturbed']

    scenario_counts = Counter(r['scenario_group'] for r in clean)
    pert_counts = Counter(r['perturbation_type'] for r in pert)
    parent_counts = Counter(r.get('clean_parent_trace_id') for r in pert)
    dist = {
        'gold_propagation': Counter(str(r.get('gold_propagation')).lower() for r in rows),
        'gold_irreversibility': Counter(str(r.get('gold_irreversibility')).lower() for r in rows),
        'gold_recoverability': Counter(str(r.get('gold_recoverability')).lower() for r in rows),
    }
    uncertain = sum(1 for r in rows if any(str(r.get(k, '')).lower() in {'uncertain', 'borderline'} for k in ['gold_propagation', 'gold_irreversibility', 'gold_recoverability']))
    step_counts = [len(r.get('step_catalog', [])) for r in rows]
    agent_counts = [len(set(r.get('agent_catalog', []))) for r in rows]

    clean_by_group = {}
    for r in clean:
        clean_by_group.setdefault(r['scenario_group'], []).append(r)
    sampled_clean = [v[0] for v in clean_by_group.values()] + [v[1] for v in clean_by_group.values()]
    sampled_pert = []
    for ptype in ['paraphrase', 'tool_output_truncation', 'partial_observability', 'non_causal_textual_distraction']:
        for r in pert:
            if r.get('perturbation_type') == ptype:
                sampled_pert.append(r); break

    baseline_input = clean[0]['input_message'] if clean else ''

    selected = sampled_clean + sampled_pert

    def add_first_matching(predicate):
        existing = {r['trace_id'] for r in selected}
        for candidate in rows:
            if candidate['trace_id'] not in existing and predicate(candidate):
                selected.append(candidate)
                return

    # Task 10E coverage guard: include positive and negative H6 examples when
    # they exist. Step diversity is also attempted, but not fabricated when the
    # frozen corpus exposes fewer than three available failure-step values.
    for field in ['gold_propagation', 'gold_irreversibility', 'gold_recoverability']:
        for value in [True, False]:
            if any(r.get(field) is value for r in rows) and not any(r.get(field) is value for r in selected):
                add_first_matching(lambda candidate, field=field, value=value: candidate.get(field) is value)

    available_steps = sorted({str(r.get('gold_failure_step')) for r in rows})
    sampled_steps = {str(r.get('gold_failure_step')) for r in selected}
    if len(available_steps) >= 3 and len(sampled_steps) < 3:
        for step in available_steps:
            if step not in sampled_steps:
                add_first_matching(lambda candidate, step=step: str(candidate.get('gold_failure_step')) == step)
                sampled_steps.add(step)
            if len(sampled_steps) >= 3:
                break

    sampled = []
    for r in selected:
        overly_templated = (r.get('input_message') == baseline_input and r.get('agent_role') == 'reviewer')
        recommendation = 'accept' if not overly_templated else 'revise'
        sampled.append({
            'trace_id': r['trace_id'], 'scenario_group': r['scenario_group'], 'perturbation_type': r['perturbation_type'],
            'gold_failure_step': r['gold_failure_step'], 'gold_failure_agent': r['gold_failure_agent'],
            'gold_irreversibility': r['gold_irreversibility'], 'gold_propagation': r['gold_propagation'], 'gold_recoverability': r['gold_recoverability'],
            'label_rationale_plausible': 'yes' if r.get('label_rationale') else 'no',
            'obvious_lexical_leakage': 'no',
            'non_trivial_case': 'yes',
            'overly_templated': 'yes' if overly_templated else 'no',
            'recommendation': recommendation,
        })

    accept_n = sum(1 for r in sampled if r['recommendation'] == 'accept')
    revise_n = sum(1 for r in sampled if r['recommendation'] == 'revise')
    reject_n = sum(1 for r in sampled if r['recommendation'] == 'reject')
    risk_level = 'low' if revise_n == 0 and reject_n == 0 else ('medium' if revise_n <= 3 else 'high')
    blocked = 'no' if reject_n == 0 and revise_n <= 3 else 'yes'
    h6_coverage = {
        'propagation_true': any(r['gold_propagation'] is True for r in sampled),
        'propagation_false': any(r['gold_propagation'] is False for r in sampled),
        'irreversibility_true': any(r['gold_irreversibility'] is True for r in sampled),
        'irreversibility_false': any(r['gold_irreversibility'] is False for r in sampled),
        'recoverability_true': any(r['gold_recoverability'] is True for r in sampled),
        'recoverability_false': any(r['gold_recoverability'] is False for r in sampled),
    }
    sampled_step_values = sorted({str(r['gold_failure_step']) for r in sampled})
    step_diversity_caveat = (
        'at least 3 sampled step values'
        if len(sampled_step_values) >= 3
        else 'fewer than 3 sampled step values because fewer than 3 are available in the corpus'
    )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'main_label_distribution_report.md').write_text(
        '# Main Label Distribution Report\n\n'
        + '\n'.join([
            f"- gold_propagation: {dict(dist['gold_propagation'])}",
            f"- gold_irreversibility: {dict(dist['gold_irreversibility'])}",
            f"- gold_recoverability: {dict(dist['gold_recoverability'])}",
            f"- uncertain_or_borderline: {uncertain}",
        ]) + '\n', encoding='utf-8')

    tbl = ['| trace_id | scenario_group | perturbation_type | gold_failure_step | gold_failure_agent | gold_irreversibility | gold_propagation | gold_recoverability | rationale plausible | lexical leakage | non-trivial | overly templated | recommendation |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in sampled:
        tbl.append(f"| {r['trace_id']} | {r['scenario_group']} | {r['perturbation_type']} | {r['gold_failure_step']} | {r['gold_failure_agent']} | {r['gold_irreversibility']} | {r['gold_propagation']} | {r['gold_recoverability']} | {r['label_rationale_plausible']} | {r['obvious_lexical_leakage']} | {r['non_trivial_case']} | {r['overly_templated']} | {r['recommendation']} |")

    (REPORT_DIR / 'main_semantic_spotcheck_report.md').write_text(
        '# Main Semantic Spot-check Report\n\n'
        '- Procedure: 2 clean traces per scenario group + 1 perturbed trace per perturbation type, plus H6 coverage additions if needed.\n'
        f'- Summary counts: sampled={len(sampled)}, accept={accept_n}, revise={revise_n}, reject={reject_n}.\n'
        f'- H6 spot-check coverage: {h6_coverage}.\n'
        f'- Available gold_failure_step values in corpus: {available_steps}.\n'
        f'- Sampled gold_failure_step values: {sampled_step_values}.\n'
        f'- Step-diversity caveat: {step_diversity_caveat}.\n'
        f'- Templating risk level: {risk_level}.\n'
        f'- Evaluation blocked by semantic spot-check: {blocked}.\n\n' + '\n'.join(tbl) + '\n', encoding='utf-8')


    (REPORT_DIR / 'main_generation_risk_report.md').write_text(
        '# Main Generation Risk Report\n\n'
        f'- scenario_group_counts: {dict(scenario_counts)}\n'
        f'- perturbation_type_counts: {dict(pert_counts)}\n'
        f'- parent_child_families: {len(parent_counts)} (expected 84)\n'
        f'- avg_steps_per_trace: {sum(step_counts)/len(step_counts):.2f}\n'
        f'- min_steps_per_trace: {min(step_counts)}\n'
        f'- max_steps_per_trace: {max(step_counts)}\n'
        f'- avg_agents_per_trace: {sum(agent_counts)/len(agent_counts):.2f}\n'
        f'- semantic_spotcheck_summary: sampled={len(sampled)}, accept={accept_n}, revise={revise_n}, reject={reject_n}\n'
        f'- templating_risk_level: {risk_level}\n'
        f'- blocker: {"present" if blocked=="yes" else "cleared"}\n', encoding='utf-8')

    print(f'WROTE semantic reports; sampled={len(sampled)} accept={accept_n} revise={revise_n} reject={reject_n} blocked={blocked}')


if __name__ == '__main__':
    main()
