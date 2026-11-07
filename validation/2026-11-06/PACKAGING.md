# Portable nominal package validation — November 6, 2026

Canonical model: `SO101ER.urdf`, copied byte-for-byte from the October 22 candidate `SO101ER.nominal.urdf`.
SHA-256: `f3be452f27274594168ee6d5a5c4378a09f7201f292290ccb9290b9de1e8b8dc`.

## Completed checks

- Working directory and clean temporary staged checkout: XML parsing, urdfdom `check_urdf`, complete tree with 8 links and 7 joints.
- All 13 unique mesh dependencies resolve within the package and match the original provenance SHA-256 manifest. No mesh bytes, vertex scales or orientations changed.
- Exact nominal URDF hash verifies every joint definition, mesh origin, mesh scale and orientation, including corrected elbow and wrist origins.
- All runtime mesh references are relative; no ROS package, WSL or workstation paths are required. Absolute paths in archived provenance describe original sources only.
- The locally validated Git trees matched the GitHub-uploaded trees. Original root-level print files are unchanged, and the previous primary URDF is retained in Git history.
- Diff review preserved original STL CRLF bytes rather than normalizing assets.

The local shell could not clone GitHub or install MuJoCo because DNS was unavailable. Publication used the connected GitHub API, preserving the existing parent commit and repository tree. Local validation used a reconstructed upstream tree whose Git tree hash matched GitHub. MuJoCo testing ran on fresh actual GitHub Actions checkouts, on Ubuntu with Python 3.12 and `mujoco==3.8.0`.

## MuJoCo 3.8.0

Direct nominal import failed with an STL decoder error on the ASCII extended-arm meshes: `number of faces should be between 1 and 200000 ... perhaps this is an ASCII file?`.
[Direct-import diagnostic run](https://github.com/gurusoft242/so101_extended_reach/actions/runs/42315395778).

The separate `tools/prepare_mujoco.py` generator preserves the canonical assets and emits `build/mujoco/SO101ER.mujoco.urdf` with local dependencies. It converts the two ASCII STLs to OBJ, preserving the decimal coordinate tokens and ordered triangles (upper: 8,038 triangles; lower: 10,508). The 11 binary stock meshes are copied unchanged. Only those mesh filename extensions and explicit MuJoCo compiler options differ in the generated URDF. No nominal geometry, inertias, limits or collision definitions are edited.

[Passing PR validation run](https://github.com/gurusoft242/so101_extended_reach/actions/runs/42315685283) and [passing branch run](https://github.com/gurusoft242/so101_extended_reach/actions/runs/42315678472), tested commit `870fba32f3bf0ba22ccde33bc76177d57898696e`:

```text
PASS: XML, 8 links / 7 joints, 13 relative mesh paths and hashes.
PASS: exact nominal URDF SHA-256; all joints, mesh scales and orientations preserved.
PASS: MuJoCo 3.8.0; nq=6, nv=6, nmesh=13, ngeom=34, actuators=0
PASS: all 7 descendant frames across 4 poses match independent URDF FK; max error=5.55e-16
No dynamics stepping, renderer or hardware commands used.
```

The generated package was also checked from a clean local staged checkout: undoing only mesh filename substitutions and removing the compiler extension reproduces the nominal XML elements exactly. CI performs the same comparison before MuJoCo import.

## Scope

The October 22 numerical/registration results and browser screenshots are historical evidence, archived separately under `validation/2026-10-22/`. Registration calculations were not rerun during packaging. No new MuJoCo rendered visual inspection was performed.

This package supports the planned November 7, 2026 Steam Fest kinematic visualization. It does not establish physical calibration, collision safety, hardware zero/sign mapping, clearance or accurate dynamics. Masses and inertias remain inherited. No robot movement or separate BISHOP application, knowledge, hardware configuration or calibration changes were made.
