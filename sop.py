import path_graph as pg
import networkx as nx


def is_advailable(graph: nx.DiGraph, node: int or str, visited_nodes: list):
    """
    Tells if node is accessable with the list of visited_nodes, with precedence constraints //
    if node is already visited -> no need to go back to it
    if parent of the node are not visited -> cannot go to this node
    """
    if node in visited_nodes:
        return False
    for parent in graph.predecessors(node):
        if not (parent in visited_nodes):
            return False
    return True


def advailable_set_of_node(graph: nx.DiGraph, graph_nodes: list, visited_node: list):
    """
    Create a set of every accessible nodes from the visited nodes
    """
    advailable = set()
    for node in graph_nodes:
        if is_advailable(graph, node, visited_node):
            advailable.add(node)
    return advailable


if __name__ == "__main__":

    print("TESTING RANGE")
    print("=========================================")

    print("extract and transform small graph...")
    small_graph_path = "./Graphs/smallRandom.json"
    small_graph, small_graph_nodes = pg.extract_directed_graph(
        small_graph_path)
    pg.transform(small_graph, small_graph_nodes)
    small_graph_nodes = [*small_graph_nodes, "start", "end"]

    print('=========================================')
    print("starting test of advailability")
    visited_node = []
    start_set = advailable_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("Used visited node list :", visited_node)
    print("We should only have start in the returned set :", start_set,
          "   then the test is good :", start_set == set(["start"]))
    visited_node = ["start"]
    start_set = advailable_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("\nUsed visited node list :", visited_node)
    print("We should only have 1 in the returned set :", start_set,
          "   then the test is good :", start_set == set([1]))
    visited_node = ["start", 1]
    start_set = advailable_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("\nUsed visited node list :", visited_node)
    print("We should only have 2,3,4 in the returned set :", start_set,
          "   then the test is good :", start_set == set([2, 3, 4]))
    visited_node = ["start", 1, 2, 3, 4, 5, 7, 9]
    start_set = advailable_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("\nUsed visited node list :", visited_node)
    print("The returned set is : ", start_set)
    print("end is not in the returned set :", not "end" in start_set)

    print("==========================================================")
    print("END")
