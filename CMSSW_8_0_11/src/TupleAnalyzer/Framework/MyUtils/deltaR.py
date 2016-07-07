import math
import copy

def deltaR2( e1, p1, e2=None, p2=None):
    """Take either 4 arguments (eta,phi, eta,phi) or two objects that have 'eta', 'phi' methods)"""
    if (e2 == None and p2 == None):
        return deltaR2(e1.eta(),e1.phi(), p1.eta(), p1.phi())
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp


def deltaR( *args ):
    return math.sqrt( deltaR2(*args) )


def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res

def vectorAdd2D(obj1_pt,obj1_phi,obj2_pt,obj2_phi):
    newPtX = obj1_pt*math.cos(obj1_phi)+obj2_pt*math.cos(obj2_phi)
    newPtY = -obj1_pt*math.sin(obj1_phi)-obj2_pt*math.sin(obj2_phi)
    newPhi = math.atan2(-newPtY,newPtX)
    newPt = math.sqrt(newPtX**2+newPtY**2)
    return newPt,newPhi

def dotProd(obj1_pt,obj1_phi,obj2_pt,obj2_phi):
    dPhi = deltaPhi(obj1_phi,obj2_phi)
    dP = obj1_pt*obj2_pt*math.cos(dPhi)
    return dP

def matchObjectCollection(recoObjects,matchCollection,deltaRMax = 0.5):

    pairs = {}

    for recoObject in recoObjects:
        recoObject.matched = False
    for match in matchCollection:
        match.matched = False

    if len(recoObjects)==0:
        return pairs
    if len(matchCollection)==0:
        # return {recoObject:None for recoObject in recoObjects}
        return dict( zip(recoObjects, [None]*len(recoObjects)) )

    allPairs = [(deltaR2 (recoObject.eta, recoObject.phi, match.eta, match.phi), (recoObject, match)) for recoObject in recoObjects for match in matchCollection]
    allPairs.sort()

    deltaR2Max = deltaRMax * deltaRMax
    for dR2, (recoObject, match) in allPairs:
        if dR2 > deltaR2Max:
            break
        if dR2 < deltaR2Max and recoObject.matched == False and match.matched == False:
            recoObject.matched = True
            match.matched = True
            pairs[recoObject] = match

    for recoObject in recoObjects:
        if recoObject.matched == False:
            pairs[recoObject] = None

    return pairs

def bestMatch( object, matchCollection):
    '''Return the best match to object in matchCollection, which is the closest object in delta R'''
    deltaR2Min = float('+inf')
    bm = None
    for match in matchCollection:
        dR2 = deltaR2( object.eta, object.phi,
                       match.eta, match.phi )
        if dR2 < deltaR2Min:
            deltaR2Min = dR2
            bm = match
    return bm, deltaR2Min
