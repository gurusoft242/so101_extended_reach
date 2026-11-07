"""Verify the portable nominal package; optionally probe MuJoCo 3.8.0."""
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'SO101ER.urdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
root = ET.parse(path).getroot()
evidence = ROOT / 'validation/2026-10-22'
validation = json.loads((evidence / 'VALIDATION.json').read_text())
assert sha(path) == validation['checks']['final_artifact_integrity']['candidate_urdf_sha256']
links, joints = root.findall('link'), root.findall('joint')
assert len(links) == 8 and len(joints) == 7
names = {link.get('name') for link in links}
children = set()
for joint in joints:
    assert joint.find('parent').get('link') in names
    child = joint.find('child').get('link')
    assert child in names and child not in children
    children.add(child)
assert names - children == {'base_link'}
meshes = {m.get('filename') for m in root.iter('mesh')}
assert len(meshes) == 13
manifest = json.loads((evidence / 'PROVENANCE.json').read_text())['files']
for name in sorted(meshes):
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts and ':' not in name
    assert sha(ROOT / p) == manifest[name]['sha256'], name
for name, xyz in [('elbow_flex', '-0.18877 -0.028 0'), ('wrist_flex', '-0.21110 0.00520 0')]:
    assert root.find(f"joint[@name='{name}']/origin").get('xyz') == xyz
print('PASS: XML, 8 links / 7 joints, 13 relative mesh paths and hashes.')
print('PASS: exact nominal URDF SHA-256; all joints, mesh scales and orientations preserved.')
if '--mujoco' in sys.argv:
    import mujoco
    assert mujoco.__version__ == '3.8.0', mujoco.__version__
    try:
        model = mujoco.MjModel.from_xml_path(str(path))
    except Exception as error:
        print('DIRECT_MUJOCO_LOAD_ERROR:', repr(error), flush=True)
        raise
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    print(f'PASS: MuJoCo {mujoco.__version__}: nq={model.nq}, nv={model.nv}, nmesh={model.nmesh}, ngeom={model.ngeom}')
