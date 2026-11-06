# SO-101 extended reach

Extended arms developed for our SO-101 chess robot when the stock reach was insufficient.

## Reference model

**`SO101ER.urdf` is the canonical corrected nominal model**, promoted from the October 22, 2026 `SO101ER.nominal.urdf` candidate. There is one editable geometry definition. The previous primary URDF remains in Git history at `e31f4bc612561ae77817b2440da7716dda52c84d`.

The 13 required meshes reside in `meshes/` (two extended arm prints) and `meshes/assets/` (11 stock components). All paths are relative to the URDF; ROS, WSL and the original workstation paths are unnecessary. Original root-level print STLs are retained for compatibility. Mesh bytes, scales, placements and joint geometry match the validated candidate exactly. The `2mm` print suffix means version 2 exported in millimetres, not a 2 mm extension. The extended prints use URDF scale `0.001 0.001 0.001`; vertices have not been rescaled.

## Fresh clone

```bash
git clone https://github.com/gurusoft242/so101_extended_reach.git
cd so101_extended_reach
python3 tools/validate_model.py
```

Use `<clone-directory>/SO101ER.urdf` in a URDF viewer that resolves mesh paths relative to the model file. For BISHOP with the clone under the home directory this is `~/so101_extended_reach/SO101ER.urdf`.

Immediate intended use: a kinematic-only MuJoCo 3.8.0 visualization mirroring SO-101 leader/follower joint positions for the November 7, 2026 Steam Fest demonstration. Joint positions must be mapped by name in radians; apply positions and call `mj_forward`, without a dynamics stepping loop or robot commands. Motor zero/sign mapping to the actual hardware is a separate calibration concern.

The pinned MuJoCo check runs in `.github/workflows/validate-model.yml` on a fresh checkout:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install mujoco==3.8.0
python tools/validate_model.py --mujoco
```

## Evidence and limitations

`validation/2026-10-22/PROVENANCE.json`, `VALIDATION.json`, `REPORT.md` and four screenshots preserve the original candidate evidence. Workstation paths there are historical provenance, never runtime dependencies. The archived report describes the candidate before publication; its statements about no commit/push and filenames refer to that earlier stage. The large standalone preview and original URDF archive are not duplicated here.

The original numerical checks passed: urdfdom parsing, 8 links / 7 joints, 13 resolved meshes, 17 matching visual/collision pairs, nominal shaft registration and four forward-kinematic poses. The packaged model also passes urdfdom and hash verification against the candidate. Exact URDF identity covers all corrected joint geometry, mesh scales and orientations; mesh hashes verify no vertex changes. The packaging script reruns structural and integrity checks; it does not recompute the archived STEP/STL registration analysis.

The prior browser inspection used four precomputed poses and actual visual triangles without decimation. It reported no obvious detached geometry. It was not an independent URDF-loader test or a collision check. Screenshots are historical evidence, not a new MuJoCo visual inspection.

This is a nominal extended-reach hardware reference, **not a physically calibrated as-built model**. Original STEP servo offsets and tilts were not adopted. Masses, centres of mass and inertias are inherited and unvalidated for dynamics. Physical clearances, self-collision, cables, fasteners, installed motor zeros and hardware replacements are not certified. Numerical consistency and appearance do not establish collision safety or accurate dynamics.
