
from subprocess import run

class Pod:
    From = None
    Pkgs = []          
    Api = None
    Tensor = None
    isAbstract = None
    def __init__(self):
        super().__init__()
        self.isAbstract = True
    
    def setFrom(self, line):
        self.From = line

    def setPkg(self, line):
        self.Pkgs.append(line)

    def setApi(self, line):
        self.Api = line
        self.isAbstract = False

    def setCtr(self, line):
        self.Contract = line

    def setTensor(self, line):
        self.Tensor = line
    
    def show(self):
        print(self.From)
        print(self.Api)
        print(self.Contract)
        print(self.Tensor)
        print(self.Pkgs)
    
    def build(self):
        pass



def makePod(filename):
    def switch(line, pod):
        s = line[0]
        if s == 'FROM':
            pod.setFrom(line[1])
        elif s == 'PKG':
            pod.setPkg(line[1:])
        elif s == 'API':
            pod.setApi(line[1:])
        elif s == 'CTR':
            pod.setCtr(line[1:])
        elif s == 'TNS':
            pod.setTensor(line[1:])
    file = open(filename, "r")
    pod = Pod()
    for l in file.readlines():
        switch( l.split(), pod )
    return pod

def isValidHyperFile(file):
    pass

if __name__ == "__main__":
    file="hyperfile.hy"
    if isValidHyperFile(file):
        pod = makePod()
        pod.show()
        pod.build()