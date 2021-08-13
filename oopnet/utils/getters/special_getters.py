def getneighbor(self, pipe):
        nodes = [pipe.startnode, pipe.endnode]
        npipes = [x for x in self.pipes if (x.startnode in nodes or x.endnode in nodes) and x.id != pipe.id]
        return npipes

def getnextneighbor(self, pipe):
    npipes = self.getneighbor(pipe)
    nnpipes = []
    for np in npipes:
        nnpipes += self.getneighbor(np)
    nnpipes = [x for x in nnpipes if x.id != pipe.id]
    for np in npipes:
        if np in nnpipes:
            nnpipes.remove(np)
    nnpipes = list(set(nnpipes))
    nnpipes.sort(key=lambda x: x.id)
    return nnpipes

def getsourcelist(self):
    """
    This function returns all sources (tanks and reservoirs) of an oopnet network
    """
    sourcelist = list()
    if self.tanks and self.reservoirs:
        sourcelist = self.tanks + self.reservoirs
    elif self.tanks:
        sourcelist = self.tanks
    elif self.reservoirs:
        sourcelist = self.reservoirs
    return sourcelist

# def getneighbornode(self, nodelist):
#     npipes = [x for x in self.pipes if (x.startnode in nodelist or x.endnode in nodelist)]
#     nnodes = list()
#     for n in npipes:
#         if n.startnode.id in nodelist:
#             nnodes.append(n.endnode)
#         else:
#             nnodes.append(n.startnode)
#     return nnodes

def getsourceneighbors(self):
    sourcelist = self.getsourcelist()
    return self.getneighbornode(sourcelist)
