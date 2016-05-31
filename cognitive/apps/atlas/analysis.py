from cognitive.settings import DOMAIN
import requests

# PAGERANK ###########################################################################

# Gets all nodes connected by some relationship and updates each node with the property key pagerank.
# The value of the pagerank property is a float data type, ex. pagerank: 3.14159265359.
# PageRank is used to find the relative importance of a node within a set of connected nodes.

# :GET /service/mazerunner/analysis/pagerank/KNOWS
def pagerank(relation="KINDOF"):

    # submit analysis to run
    url = "%s/service/mazerunner/analysis/pagerank/%s" %(DOMAIN,relation)
    result = run_analysis(url)

# CLOSENESS_CENTRALITY ###############################################################

# Gets all nodes connected by the FOLLOWS relationship and updates each node with the property key closeness_centrality.
# The value of the closeness_centrality property is a float data type, ex. pagerank: 0.1337.
# A key node centrality measure in networks is closeness centrality (Freeman, 1978; Opsahl et al., 2010; Wasserman and Faust, 1994). It is defined as the inverse of farness, which in turn, is the sum of distances to all other nodes.

# :GET /service/mazerunner/analysis/closeness_centrality/MEASUREDBY
def closeness_centrality(relation="MEASUREDBY"):

    # submit analysis to run
    url = "%s/service/mazerunner/analysis/closeness_centrality/%s" %(DOMAIN,relation)
    result = run_analysis(url)

# BETWEENNESS_CENTRALITY #############################################################

# Gets all nodes connected by some relationship and updates each node with the property key betweenness_centrality.
# The value of the betweenness_centrality property is a float data type, ex. betweenness_centrality: 20.345.
# Betweenness centrality is an indicator of a node's centrality in a network. It is equal to the number of shortest paths from all vertices to all others that pass through that node. A node with high betweenness centrality has a large influence on the transfer of items through the network, under the assumption that item transfer follows the shortest paths.

# :GET /service/mazerunner/analysis/betweenness_centrality/MEASUREDBY
def betweenness_centrality(relation="MEASUREDBY"):

    # submit analysis to run
    url = "%s/service/mazerunner/analysis/betweenness_centrality/%s" %(DOMAIN,relation)
    result = run_analysis(url)

# TRIANGLE_COUNTING ##################################################################

# :GET /service/mazerunner/analysis/triangle_count/MEASUREDBY

# Gets all nodes connected by some relationship and updates each node with the property key triangle_count.
# The value of the triangle_count property is an integer data type, ex. triangle_count: 2.
# The value of triangle_count represents the count of the triangles that a node is connected to.
# A node is part of a triangle when it has two adjacent nodes with a relationship between them. The triangle_count property provides a measure of clustering for each node.

def triangle_count(relation="MEASUREDBY"):

    # submit analysis to run
    url = "%s/service/mazerunner/analysis/triangle_count/%s" %(DOMAIN,relation)
    result = run_analysis(url)

# CONNECTED_COMPONENTS ###############################################################

# :GET /service/mazerunner/analysis/connected_components/MEASUREDBY

# Gets all nodes connected by the FOLLOWS relationship and updates each node with the property key connected_components.
# The value of connected_components property is an integer data type, ex. connected_components: 181.
# The value of connected_components represents the Neo4j internal node ID that has the lowest integer value for a set of connected nodes.
# Connected components are used to find isolated clusters, that is, a group of nodes that can reach every other node in the group through a bidirectional traversal.

def connected_components(relation="MEASUREDBY"):

    # submit analysis to run
    url = "%s/service/mazerunner/analysis/connected_components/%s" %(DOMAIN,relation)
    result = run_analysis(url)

# STRONGLY_CONNECTED_COMPONENTS ######################################################

# :GET /service/mazerunner/analysis/strongly_connected_components/MEASUREDBY

# Gets all nodes connected by some relationship and updates each node with the property key strongly_connected_components.
# The value of strongly_connected_components property is an integer data type, ex. strongly_connected_components: 26.
# The value of strongly_connected_components represents the Neo4j internal node ID that has the lowest integer value for a set of strongly connected nodes.
# Strongly connected components are used to find clusters, that is, a group of nodes that can reach every other node in the group through a directed traversal.

def strongly_connected_components(relation="MEASUREDBY"):

    # submit analysis to run
    url = "%s/service/mazerunner/analysis/strongly_connected_components/%s" %(DOMAIN,relation)
    result = run_analysis(url)


def run_analysis(url)
    '''run_analysis will submit a GET request to run a graph analysis with Mazerunner (under development)
    :param url: the url of the request for GET.
    '''
    response = requests.get(url)
    result = None
    if response.status_code == 200:
        result = response.json()
    return result    

# Eg, how to get a result after submit -problems need to figure out:
# 1) Under what context should different analyses be run for Cogat?
# 2) How often should analyses be run, and how? (eg, daily celery job vs. on request)
# 3) How do we know when the analysis has finished (and results are available?)
#
# and how do we implement different similarity metrics for nodes? (eg, wang)
#
# MATCH (p:Person) WHERE has(p.pagerank) AND has(p.closeness_centrality)
# RETURN p.name, p.pagerank as pagerank, p.closeness_centrality
# ORDER BY pagerank DESC
