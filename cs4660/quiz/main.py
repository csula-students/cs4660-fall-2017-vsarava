"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = json.load(urlopen(req, jsondataasbytes))
    return response

def bfs(start, end):
    """
    Breadth First Search
    queries the game to do search from the start to end
    returns a list of path going from the start to end
    """
    q = []
    q.append((0, start));
    distance_of = {}
    distance_of[start] = 0
    parent_of = {}
    edge_to = {}

    while len(q) > 0:
        node = get_state(q.pop()[1])
        neighbors = node['neighbors']
        for i in range(len(neighbors)):
            neigh = neighbors[i]
            if neigh['id'] not in distance_of:
                edge = transition_state(node['id'], neigh['id'])
                edge_to[neigh['id']] = edge
                distance_of[neigh['id']] = distance_of[node['id']] + 1
                parent_of[neigh['id']] = node['id']
                if neigh['id'] != end:
                    q.append((distance_of[neigh['id']], neigh['id']))
        q = sorted(q, key=lambda x:x[0])
        q.reverse()

    path = []
    node_id = end
    while node_id in parent_of:
        path.append(edge_to[node_id])
        node_id = parent_of[node_id]
    path.reverse()
    return path

def dijkstra(start, end):
    """
    Dijkstra Search
    queries the game to do search from the init_node to dest_node
    returns a list of path going from the init_node to dest_node
    """
    q = []
    q.append((0, start))
    visited = []
    distance_of = {}
    distance_of[start] = 0
    previous_of = {}
    edge_to = {}

    while len(q) > 0:
        node = get_state(q.pop()[1])
        visited.append(node['id'])
        neighbors = node['neighbors']
        for i in range(len(neighbors)):
            neigh = neighbors[i]
            edge = transition_state(node['id'], neigh['id'])
            alt = distance_of[node['id']] + edge['event']['effect']
            if neigh['id'] not in visited and (neigh['id'] not in distance_of or alt > distance_of[neigh['id']]):
                if neigh['id'] in distance_of:
                    q.remove((distance_of[neigh['id']], neigh['id']))
                q.append((alt, neigh['id']))
                distance_of[neigh['id']] = alt
                previous_of[neigh['id']] = node['id']
                edge_to[neigh['id']] = edge
        q = sorted(q, key=lambda x:x[0])
    
    path = []
    node_id = end
    while node_id in previous_of:
        path.append(edge_to[node_id])
        node_id = previous_of[node_id]

    path.reverse()
    return path

def print_path(path, start):
    prev_id = start
    total = 0
    for i in range(len(path)):
        prev_node = get_state(prev_id)
        next_id = path[i]['id']
        total += path[i]['event']['effect']
        print("%s(%s):%s(%s):%i" % (prev_node['location']['name'], prev_id, path[i]['action'], path[i]['id'], path[i]['event']['effect']))
        prev_id = next_id
    print("\nTotal HP: %i" % total)

if __name__ == "__main__":
    start = '7f3dc077574c013d98b2de8f735058b4'
    end = 'f1f131f647621a4be7c71292e79613f9'
    
    path = bfs(start, end)
    print("\nBFS Path:")
    print_path(path, start)

    path = dijkstra(start, end)
    print("\nDijkstra Path:")
    print_path(path, start)