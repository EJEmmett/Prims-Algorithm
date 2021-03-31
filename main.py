from Matrix import Matrix
from Timer import elapsed
from adj_lists import adj_lists


def main():
    for adj_list in adj_lists:
        adj_matrix = Matrix(adj_list)
        print("Graph Adjacency Matrix: ")
        print(adj_matrix)

        mst = adj_matrix.prims(timed=True)
        print(f"n: {len(adj_matrix)}\n"
              f"Basic operations: {mst.basic_ops}\n"
              f"Elapsed Time: {elapsed(mst)}\n")
        print("Minimum spanning tree: ")
        print(mst)


if __name__ == "__main__":
    main()
