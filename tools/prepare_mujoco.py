"""Generate a disposable MuJoCo package without editing nominal model/assets."""
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def ascii_stl_to_obj(source, target):
    # Keep decimal coordinate tokens exactly; avoid float32 STL re-encoding.
    vertices = [line.split()[1:] for line in source.read_text().splitlines()
                if line.strip().startswith('vertex ')]
    assert vertices and len(vertices) % 3 == 0
    assert all(len(v) == 3 for v in vertices)
    lines = ['# Generated from authoritative ASCII STL; coordinates unchanged.']
    lines += ['v ' + ' '.join(v) for v in vertices]
    lines += [f'f {i+1} {i+2} {i+3}' for i in range(0, len(vertices), 3)]
    target.write_text('\n'.join(lines) + '\n')
    # Verify exact ordered triangles in the emitted file.
    emitted = [line.split()[1:] for line in target.read_text().splitlines() if line.startswith('v ')]
    assert emitted == vertices
    return len(vertices) // 3


def prepare(output=None):
    output = Path(output) if output else ROOT / 'build/mujoco'
    output.mkdir(parents=True, exist_ok=True)
    tree = ET.parse(ROOT / 'SO101ER.urdf')
    root = tree.getroot()
    mapping = {}
    for name in sorted({m.get('filename') for m in root.iter('mesh')}):
        source = ROOT / name
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.read_bytes().startswith(b'solid ASCII'):
            target = target.with_suffix('.obj')
            faces = ascii_stl_to_obj(source, target)
            print(f'ASCII STL -> OBJ: {name}, {faces} triangles; exact decimal vertices')
            mapping[name] = str(Path(name).with_suffix('.obj'))
        else:
            shutil.copyfile(source, target)
    for mesh in root.iter('mesh'):
        mesh.set('filename', mapping.get(mesh.get('filename'), mesh.get('filename')))
    # Explicit import settings retain visual meshes and fixed tool-frame bodies.
    extension = ET.SubElement(root, 'mujoco')
    ET.SubElement(extension, 'compiler', strippath='false', discardvisual='false', fusestatic='false')
    result = output / 'SO101ER.mujoco.urdf'
    tree.write(result, encoding='utf-8', xml_declaration=True)
    print('Generated:', result)
    return result


if __name__ == '__main__':
    prepare()
