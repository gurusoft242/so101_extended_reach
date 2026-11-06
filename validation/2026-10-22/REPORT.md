# BISHOP corrected nominal SO101ER candidate

The isolated candidate implements the requested geometry. Original project files are preserved. No commit, push, ROS simulation, or hardware command was performed.

## Locations and provenance

Candidate: /home/guru/bishop_candidates/so101er_nominal_e31f4bc

Windows: \\wsl.localhost\Ubuntu\home\guru\bishop_candidates\so101er_nominal_e31f4bc

- SO101ER.nominal.urdf: corrected model with self-contained relative mesh paths.
- SO101ER.original.urdf: exact source archive, with original package paths.
- meshes/: 13 unique files; authoritative millimetre STLs plus 11 inherited stock meshes.
- PROVENANCE.json: original sources, full SHA-256 hashes, pinned revision, and exact edits.
- VALIDATION.json: detailed numerical checks.
- preview.html: offline browser preview with four selectable virtual poses.
- browser-pose-0.png through browser-pose-3.png: inspected Chrome screenshots.

Authoritative repository: https://github.com/gurusoft242/so101_extended_reach
Pinned revision: e31f4bc612561ae77817b2440da7716dda52c84d
Print-file addition: c7e043e58c0cb4fe0dfb5a93b93b460079c74833

The 2mm suffix means version 2 exported in millimetres, not a 2 mm extension.
The authoritative STL vertices and file hashes are unchanged.

## Changes

All translations below are metres.

| Element | Original xyz | Corrected xyz |
|---|---|---|
| elbow_flex joint | -0.16316 -0.04058 ~0 | -0.18877 -0.028 0 |
| wrist_flex joint | -0.18592 0.00717 ~0 | -0.21110 0.00520 0 |
| Upper printed mesh | -0.065085 0.012 0.0182 | -0.15707842 -0.00075000 0.01865001 |
| Lower printed mesh | -0.0648499 -0.032 0.0182 | -0.20644990 -0.32000000 0.00020000 |
| Elbow motor | -0.11257 -0.0155 0.0187 | -0.18877 -0.0155 0.0187 |
| Wrist motor holder | -0.0648499 -0.032 0.018 | -0.1410499 -0.032 0.018 |
| Wrist motor | -0.1224 0.0052 0.0187 | -0.1986 0.0052 0.0187 |

Both printed meshes now reference the authoritative version-2 STL basenames in meshes/, use scale 0.001 0.001 0.001, and RPY 3.141592653589793 0 0. Both visual and collision elements were updated. The previously translated C: lower STL is not used.

All stock mesh paths were made relative and resolve inside this folder. Joint RPY, axes and limits were preserved. Motor and holder rotations were preserved. Other joints, gripper/tool relationships and descendant-local geometry were not extended again.

## Numerical validation

| Check | Result |
|---|---|
| Independent urdfdom check_urdf | Passed; complete tree, 8 links, 7 joints |
| Mesh paths | All 13 unique files resolve locally |
| Visual/collision placements | All 17 pairs match |
| Upper separation | 190.835303075715 mm |
| Lower separation | 211.164035763669 mm |
| Upper incoming/outgoing shaft position residual | 0.000007956 / 0.000002242 mm |
| Lower incoming/outgoing shaft position residual | 0.000025282 / 0.000012604 mm |
| Nominal unoriented shaft-axis angular residual | 0 degrees to numerical reporting precision |
| Upper motor/pocket common-shift residual | 0.000052024 mm |
| Lower motor/holder mounting-frame common-shift residual | 0.000118820 mm |
| FK rotation orthogonality, four poses | At most 7.78e-16 |
| Gripper tool relative-transform residual, four poses | At most 2.23e-16 |

The shaft residuals are based on actual STL horn circles and STEP/STL mounting-landmark registration, with the upstream nominal shaft datums transferred through that registration. They are numerical consistency residuals, not manufacturing tolerances or measurements of the installed machine. Motor-frame residuals compare the registered printed interfaces with the prescribed 76.2 mm common translation; they do not certify fastener fit or clearances.

## Browser inspection

The offline preview rendered successfully in installed Windows Chrome for zero, reach, fold and opposite configurations. DOM readiness was verified, screenshots were captured, and the views were inspected. No obvious detached geometry was seen at the shoulder, elbow, wrist holder or gripper.

The preview uses the actual triangles without decimation, but projects them in advance from the validated FK configurations. It is not an independent browser URDF parser or collision checker. The gkjohnson viewer itself was not executed.

For offline viewing, open preview.html in Chrome or Edge and select the pose buttons.

For arbitrary virtual joint controls:
1. Open https://gkjohnson.github.io/urdf-loaders/javascript/example/bundle/ in Chrome.
2. Drag SO101ER.nominal.urdf and the meshes folder together into the viewer.
3. Select the nominal file explicitly if needed; do not select SO101ER.original.urdf.
4. Keep joint limits enabled. Toggle collision display to compare placements.
5. Start at zero, then use the pose values recorded in VALIDATION.json.

No local server or ROS process is necessary for the offline preview.

## Remaining limitations

This is a nominal upstream-interface geometry model, not as-built calibration. The original STEP assembly's small saved servo offsets and tilts were not adopted. Masses, centres of mass and inertias remain inherited; they require revision before dynamics. Self-collision, physical clearances, cable routing, fasteners, actual motor zero calibration and replacement history are not validated.

No original URDF was replaced, and no commit or push was made.
