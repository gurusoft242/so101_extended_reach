"""Check direct import, derived import and kinematics; never step dynamics."""
import json
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import mujoco
import numpy as np
from prepare_mujoco import ROOT, prepare

assert mujoco.__version__ == '3.8.0'
source = ROOT / 'SO101ER.urdf'
try:
    mujoco.MjModel.from_xml_path(str(source))
except ValueError as error:
    assert 'stl_decoder' in str(error) and 'ASCII' in str(error), str(error)
    print('EXPECTED_DIRECT_IMPORT_LIMITATION:', str(error), flush=True)
else:
    raise AssertionError('Expected ASCII STL rejection changed; review adaptation')


def rotation(rpy):
    r, p, y = rpy
    cr, cp, cy = np.cos([r, p, y])
    sr, sp, sy = np.sin([r, p, y])
    return np.array([[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr],
                     [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr],
                     [-sp, cp*sr, cp*cr]])


with tempfile.TemporaryDirectory(prefix='so101er-mujoco-') as temp:
    adapted = prepare(Path(temp))
    nominal = ET.parse(source).getroot()
    derived = ET.parse(adapted).getroot()
    # Revert only filename substitutions and remove the compiler extension.
    derived.remove(derived.find('mujoco'))
    for old, new in zip(nominal.iter('mesh'), derived.iter('mesh')):
        new.set('filename', old.get('filename'))
    assert ET.tostring(nominal) == ET.tostring(derived)
    model = mujoco.MjModel.from_xml_path(str(adapted))
    assert model.nq == model.nv == 6 and model.nu == 0 and model.nmesh == 13
    data = mujoco.MjData(model)
    poses = json.loads((ROOT / 'validation/2026-10-22/VALIDATION.json').read_text())['checks']['poses']
    max_error = 0.0
    for pose in poses:
        data.qpos[:] = 0
        for name, value in pose['radians'].items():
            data.qpos[model.joint(name).qposadr[0]] = value
        mujoco.mj_forward(model, data)
        transforms = {'base_link': np.eye(4)}
        pending = list(nominal.findall('joint'))
        while pending:
            for joint in pending[:]:
                parent = joint.find('parent').get('link')
                if parent not in transforms:
                    continue
                child = joint.find('child').get('link')
                origin = joint.find('origin')
                transform = np.eye(4)
                transform[:3, 3] = np.fromstring(origin.get('xyz', '0 0 0'), sep=' ')
                transform[:3, :3] = rotation(np.fromstring(origin.get('rpy', '0 0 0'), sep=' '))
                if joint.get('type') != 'fixed':
                    axis = np.fromstring(joint.find('axis').get('xyz'), sep=' ')
                    axis /= np.linalg.norm(axis)
                    angle = pose['radians'].get(joint.get('name'), 0)
                    x, y, z = axis
                    skew = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
                    transform[:3, :3] = transform[:3, :3] @ (np.eye(3) + np.sin(angle)*skew + (1-np.cos(angle))*(skew@skew))
                transforms[child] = transforms[parent] @ transform
                body = data.body(child)
                error = max(np.max(np.abs(body.xpos - transforms[child][:3, 3])),
                            np.max(np.abs(body.xmat.reshape(3, 3) - transforms[child][:3, :3])))
                max_error = max(max_error, float(error))
                pending.remove(joint)
        assert np.isfinite(data.xpos).all()
    assert max_error < 1e-10, max_error
    print(f'PASS: MuJoCo {mujoco.__version__}; nq={model.nq}, nv={model.nv}, nmesh={model.nmesh}, ngeom={model.ngeom}, actuators={model.nu}')
    print(f'PASS: all 7 descendant frames across 4 poses match independent URDF FK; max error={max_error:.3g}')
    print('No dynamics stepping, renderer or hardware commands used.')
