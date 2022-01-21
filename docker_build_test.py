import os
from random import randint
from subprocess import check_output
import celaut_pb2, gateway_pb2

def write_item(b: celaut_pb2.Service.Container.Filesystem.ItemBranch, dir: str):
    if b.HasField('filesystem'):
        os.mkdir(dir + b.name)
        write_fs(fs = b.filesystem, dir = dir + b.name + '/')

    elif b.HasField('file'):
        open(dir + b.name, 'wb').write(
            b.file
        )
        
    else:
        os.symlink(
            src = b.link.src,
            dst = b.link.dst
        )

def write_fs(fs: celaut_pb2.Service.Container.Filesystem, dir: str):
    for branch in fs.branch:
        write_item(
            b = branch,
            dir = dir
        )

service_with_meta = gateway_pb2.ServiceWithMeta()
service_with_meta.ParseFromString(
    open('__registry__/b11074a440261eee100bb8751610be5c5cf6efdf9a9a1128de7d61dd93dc0fd9', 'rb').read()
)

fs = celaut_pb2.Service.Container.Filesystem()
fs.ParseFromString(
    service_with_meta.service.container.filesystem
)

try:
    os.mkdir('__hycache__')
except: pass

id = str(randint(1,999))
dir = '__hycache__/builder'+id
os.mkdir(dir)
fs_dir = dir + '/fs'
os.mkdir(fs_dir)
write_fs(fs = fs, dir = fs_dir + '/')

open(dir+'/Dockerfile', 'w').write('FROM scratch\nCOPY fs .\nENTRYPOINT /random/start.py')
check_output('docker build -t '+id+' '+dir+'/.', shell=True)

