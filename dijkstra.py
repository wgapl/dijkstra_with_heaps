#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

def parent(i): 
    return (i-1)/2

def left_child(i): 
    return 2*i+1

def right_child(i): 
    return 2*i+2

def swapper(heap, prev, post, loc):
    loc[heap[prev]] = post
    loc[heap[post]] = prev
    (heap[prev], heap[post]) = (heap[post], heap[prev])
    
def down_heaper(heap, k, loc):
    while True:
        le = left_child(k)
        ri = right_child(k)
        if le >= len(heap):
            break
        v = heap[k][0]
        lv = heap[le][0]
        if ri == len(heap):
            if v > lv:
                swapper(heap,k,le,loc)
            break
        rv = heap[ri][0]
        if min(lv,rv) >= v:
            break
        if lv < rv:
            swapper(heap,k,le,loc)
            k = le
        else:
            swapper(heap,k,ri,loc)
            k = ri
            
def up_heaper(heap, k, loc):
    while k > 0:
        p = parent(k)
        if heap[k][0] < heap[p][0]:
            swapper(heap,k,p,loc)
            k = p
        else:
            break

def minpop(heap, loc):
    val = heap[0] 
    top = heap.pop()
    loc[val] = None
    if len(heap) == 0:
        return val
    loc[top] = 0
    heap[0] = top
    down_heaper(heap, 0, loc)
    return val

def inserter(heap, v, loc):
    heap.append(v)
    loc[v] = len(heap) - 1
    up_heaper(heap,len(heap)-1,loc)

def decrease_val(heap, loc, prev, post):
    k = loc[prev]
    heap[k] = post
    loc[prev] = None
    loc[post] = k
    up_heaper(heap, k, loc)
    
def dijkstra(G, a):
    first = (0, a)
    heap = [first]
    loc = {first:0}
    dist_so_far = {a:first}
    final = {}
    while len(dist_so_far) > 0:
        d, node = minpop(heap,loc)
        final[node] = d
        del dist_so_far[node]
        for x in G[node]:
            if x in final:
                continue
            nd = G[node][x] + final[node]
            entry = (nd, x)
            if x not in dist_so_far:
                inserter(heap, entry, loc)
                dist_so_far[x] = entry
            elif entry < dist_so_far[x]:
                decrease_val(heap,loc,dist_so_far[x], entry)
                dist_so_far[x] = entry
    return final
def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 1000000
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node

def dijkstra_slow(G,v):
    dist_so_far = {}
    dist_so_far[v] = 0
    final_dist = {}
    while len(final_dist) < len(G):
        w = shortest_dist_node(dist_so_far)
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist

############
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)

test()




