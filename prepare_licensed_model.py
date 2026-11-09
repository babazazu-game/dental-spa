"""Extract a licensed BodyParts3D lower molar, preserving its anatomy."""
from pathlib import Path
import json,struct,shutil
root=Path(__file__).parent
data=(root/'reference-models/bodyparts-teeth.glb').read_bytes()
size=struct.unpack_from('<I',data,12)[0]
doc=json.loads(data[20:20+size]);binary=data[28+size:]
def accessor(index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
    width={'SCALAR':1,'VEC3':3}[a['type']];fmt={5126:'f',5125:'I',5123:'H'}[a['componentType']]
    offset=v.get('byteOffset',0)+a.get('byteOffset',0)
    stride=v.get('byteStride',struct.calcsize('<'+fmt)*width)
    return [struct.unpack_from('<'+fmt*width,binary,offset+i*stride) for i in range(a['count'])]
primitive=doc['meshes'][19]['primitives'][0]
verts=accessor(primitive['attributes']['POSITION']);faces=accessor(primitive['indices'])
center=[(min(v[k] for v in verts)+max(v[k] for v in verts))/2 for k in range(3)]
scale=3.7/(max(v[1] for v in verts)-min(v[1] for v in verts))
positions=[(v[k]-center[k])*scale for v in verts for k in range(3)]
indices=[v[0] for v in faces]
(root/'dist/assets/licensed-tooth.bin').write_bytes(struct.pack('<II',len(verts),len(indices))+struct.pack('<%sf'%len(positions),*positions)+struct.pack('<%sI'%len(indices),*indices))
credit=(root/'reference-models/ATTRIBUTION.md').read_text(encoding='utf-8')
credit+='\nDental Spa concept: selected lower-left first molar, recentered and uniformly scaled; ivory material and static studio lighting. Runtime derivative: licensed-tooth.bin, CC BY-SA 2.1 Japan.\n'
(root/'dist/assets/MODEL_ATTRIBUTION.md').write_text(credit,encoding='utf-8')
print('Prepared licensed molar:',len(verts),'vertices')
