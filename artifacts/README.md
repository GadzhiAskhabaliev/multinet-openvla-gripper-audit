# Experiment archive

Archived outputs of the MultiNet v0.1 / OpenVLA baseline runs and the gripper-audit inputs.
Downloaded outputs were not edited.

| Path | Contents |
| --- | --- |
| [baseline_audit/current/output/](baseline_audit/current/output/) | All 7838 Jaco Play predictions, result, manifest, environment freeze, original log |
| [baseline_audit/current/status.json](baseline_audit/current/status.json) | Last saved baseline status, `COMPLETE` |
| [baseline_audit/verified_jaco_result.json](baseline_audit/verified_jaco_result.json) | Independent audit of the full baseline |
| [baseline_audit/submitted_v3/](baseline_audit/submitted_v3/) | Source and metadata of the completed baseline v3, downloaded from Kaggle |
| [baseline_audit/source_pin.json](baseline_audit/source_pin.json) | MultiNet commit and hashes of the original files |
| [baseline_audit/jaco_dataset_info.json](baseline_audit/jaco_dataset_info.json) | Metadata of the official Jaco Play split |
| [checksums.json](checksums.json) | SHA-256 of the archived Kaggle outputs |
| [multinet_audit/](multinet_audit/) | MultiNet pipeline re-runs on Berkeley UR5 and NYU Door Opening (predictions, result, manifest), target statistics for five datasets, step-aligned observed gripper states for Jaco Play and UR5 |

Files named `upstream_reference_NOT_OUR_RESULT.json` contain MultiNet's **published** results and
must not be presented as new runs. The folder name `current` is the historical name of the
completed baseline v3, not an auto-updated state.

## `predictions.jsonl`

One line per step: `episode`, `step` (zero-based), `image_sha256`, `instruction`,
`raw_prediction` (7-D OpenVLA output), `prediction` (after MultiNet's `convert_action`), `target`
(MultiNet target; 4-D for Jaco Play, 7-D for UR5 and NYU Door), `mse`, `inference_seconds`,
`is_last`. The gripper is the first coordinate of `prediction` and `target`.
