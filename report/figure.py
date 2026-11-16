"""Figure of the PDF report, computed from the archived predictions. Requires matplotlib.

Usage: python report/figure.py   (writes report/figure.svg and prints the numbers quoted in the report)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments/offline'))
from gripper_semantics import DEFAULT_FILES, report  # noqa: E402

NAMES = ['Jaco Play', 'Berkeley UR5', 'NYU Door Opening']
ZEROS, GRIPPER, OTHER, FIX1, FIX2, INK = '#a9b3b8', '#c0392b', '#5d6d7e', '#2471a3', '#17a589', '#1f2933'


def main():
    reports = [report(f) for f in DEFAULT_FILES[:3]]
    plt.rcParams.update({'font.family': ['Helvetica Neue', 'Helvetica', 'Arial'], 'font.size': 8,
                         'svg.fonttype': 'none', 'axes.edgecolor': INK, 'text.color': INK,
                         'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK})
    fig, ax = plt.subplots(figsize=(7.0, 2.15))
    w = 0.2
    for i, (name, r) in enumerate(zip(NAMES, reports)):
        published = r['multinet_targets']['openvla_greedy']
        fix1 = r['openvla_semantics_targets']['openvla_greedy']['amse']
        zeros = r['constant_predictors']['multinet_targets']['zeros']
        constant = r['constant_predictors']['openvla_semantics_targets']['per_dimension_mean']
        fix2 = (r['state_to_command_alignment'] or {}).get('amse')
        x = [i - 1.5 * w, i - 0.5 * w, i + 0.5 * w, i + 1.5 * w]
        ax.bar(x[0], zeros, w, color=ZEROS)
        ax.bar(x[1], published['gripper_part'], w, color=GRIPPER)
        ax.bar(x[1], published['other_dims_part'], w, bottom=published['gripper_part'], color=OTHER)
        ax.bar(x[2], fix1, w, color=FIX1)
        labels = [(x[0], zeros, f'{zeros:.3f}'), (x[1], published['amse'], f'{published["amse"]:.3f}'),
                  (x[2], fix1, f'{fix1:.3f}')]
        if fix2 is None:
            ax.text(x[3], 0.004, 'n/a', ha='center', va='bottom', color='#7b8794')
        else:
            ax.bar(x[3], fix2, w, color=FIX2)
            labels.append((x[3], fix2, f'{fix2:.3f}'))
        for xi, yi, text in labels:
            ax.text(xi, yi + 0.004, text, ha='center', va='bottom')
        floor = r['no_change_target_share'] / r['target_dim']
        print(f'{name}: published {published["amse"]:.4f}, gripper share {published["gripper_part"] / published["amse"]:.1%}, '
              f'zeros {zeros:.4f} (published / zeros = {published["amse"] / zeros:.1f}x), fix 1 {fix1:.4f}, '
              f'best constant on fix-1 targets {constant:.4f} (constant / fix 1 = {constant / fix1:.1f}x), fix 2 {fix2}, '
              f'no-change share {r["no_change_target_share"]:.3%}, dim {r["target_dim"]}, '
              f'no-change floor {floor:.4f} = {floor / published["amse"]:.1%} of published, '
              f'gripper values {r["predicted_gripper_values"][:4]}')
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (ZEROS, GRIPPER, OTHER, FIX1, FIX2)]
    ax.legend(handles, ['All-zeros predictor', 'OpenVLA as published: gripper error',
                        'OpenVLA as published: other dimensions', 'Fix 1: targets converted to states',
                        'Fix 2: predictions converted to commands'],
              frameon=False, loc='upper right', handlelength=1.0, handleheight=0.9, labelspacing=0.35)
    ax.set_xticks(range(3), NAMES, fontsize=9)
    ax.set_ylabel('AMSE (lower is better)')
    ax.set_ylim(0, 0.27)
    ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25])
    ax.tick_params(axis='x', length=0)
    ax.yaxis.grid(True, color='#e4e7eb', linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis='y', length=0)
    fig.tight_layout(pad=0.3)
    fig.savefig(Path(__file__).with_name('figure.svg'))


if __name__ == '__main__':
    main()
