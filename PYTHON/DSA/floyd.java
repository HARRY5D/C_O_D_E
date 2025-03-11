import java.util.Scanner;

public class floyd {
    final static int INF = 99999; // Large value representing Infinity

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Take input for the number of vertices
        System.out.print("Enter the number of vertices: ");
        int V = sc.nextInt();

        // Create the adjacency matrix
        int[][] graph = new int[V][V];

        System.out.println("Enter the adjacency matrix (use " + INF + " for Infinity):");
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                graph[i][j] = sc.nextInt();
            }
        }

        // Call the Floyd-Warshall algorithm
        floydWarshall(graph, V);
    }

    static void floydWarshall(int[][] dist, int V) {
        // Implement the Floyd-Warshall Algorithm
        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {
                    if (dist[i][k] != INF && dist[k][j] != INF && dist[i][j] >= dist[i][k] + dist[k][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }

        // Print the solution
        printSolution(dist, V);
    }

    static void printSolution(int[][] dist, int V) {
        System.out.println("Shortest distances between every pair of vertices:");
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (dist[i][j] == INF) {
                    System.out.print("INF ");
                } else {
                    System.out.print(dist[i][j] + " ");
                }
            }
            System.out.println();
        }
    }
}
