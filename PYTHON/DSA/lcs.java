public class lcs {
    public static void main(String[] args) {
        String X = "ABCBDAB";
        String Y = "BDCAB";
        int m = X.length();
        int n = Y.length();

        int[][] c = new int[m + 1][n + 1]; // Length table
        char[][] b = new char[m + 1][n + 1]; // Direction table

        // Fill the tables
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0 || j == 0) {
                    c[i][j] = 0; // Base case
                } else if (X.charAt(i - 1) == Y.charAt(j - 1)) {
                    c[i][j] = c[i - 1][j - 1] + 1;
                    b[i][j] = '-';
                } else if (c[i - 1][j] >= c[i][j - 1]) {
                    c[i][j] = c[i - 1][j];
                    b[i][j] = '↑';
                } else {
                    c[i][j] = c[i][j - 1];
                    b[i][j] = '←';
                }
            }
        }

        System.out.println("LCS Length: " + c[m][n]);
        System.out.print("LCS: ");
        printLCS(b, X, m, n);
    }

    // Helper function to print the LCS
    static void printLCS(char[][] b, String X, int i, int j) {
        if (i == 0 || j == 0) return;
        if (b[i][j] == '-') {
            printLCS(b, X, i - 1, j - 1);
            System.out.print(X.charAt(i - 1));
        } else if (b[i][j] == '↑') {
            printLCS(b, X, i - 1, j);
        } else {
            printLCS(b, X, i, j - 1);
        }
    }
}
