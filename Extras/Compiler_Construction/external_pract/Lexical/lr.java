import java.util.*;

public class lr {

    static String[][] action = {
            {"s5", "", "", "s4", ""},
            {"", "s6", "", "", "acc"},
            {"", "r2", "s7", "", "r2"},
            {"", "r4", "r4", "", "r4"},
            {"s5", "", "", "s4", ""},
            {"", "r6", "r6", "", "r6"},
            {"s5", "", "", "s4", ""},
            {"s5", "", "", "s4", ""},
            {"", "s6", "", "", ""},
            {"", "r1", "s7", "", "r1"},
            {"", "r3", "r3", "", "r3"},
            {"", "r5", "r5", "", "r5"}
    };

    static int[][] goTo = {
            {1, 2, 3},
            {-1, -1, -1},
            {-1, -1, -1},
            {-1, -1, -1},
            {8, 2, 3},
            {-1, -1, -1},
            {-1, 9, 3},
            {-1, -1, 10},
            {-1, -1, -1},
            {-1, -1, -1},
            {-1, -1, -1},
            {-1, -1, -1}
    };

    static String[] productions = {
            "S->A",
            "A->A+B",
            "A->B",
            "B->B*C",
            "B->C",
            "C->(A)",
            "C->id"
    };

    static Map<String, Integer> colMap = new HashMap<>();

    static {
        colMap.put("id", 0);
        colMap.put("+", 1);
        colMap.put("*", 2);
        colMap.put("(", 3);
        colMap.put("$", 4);
    }
    static void printParsingTable() {
        String[] terminals = {"id", "+", "*", "(", "$"};
        String[] nonTerminals = {"A", "B", "C"};

        System.out.println("\n LR(0) PARSING TABLE ");
        System.out.printf("%-6s", "State");
        for (String t : terminals) System.out.printf("%-6s", t);
        for (String nt : nonTerminals) System.out.printf("%-6s", nt);
        System.out.println();

        for (int i = 0; i < action.length; i++) {
            System.out.printf("%-6d", i);

            // ACTION
            for (int j = 0; j < action[i].length; j++) {
                String val = action[i][j];
                System.out.printf("%-6s", val.equals("") ? "-" : val);
            }

            // GOTO
            for (int j = 0; j < goTo[i].length; j++) {
                int val = goTo[i][j];
                System.out.printf("%-6s", val == -1 ? "-" : val);
            }

            System.out.println();
        }
    }
    public static void main(String[] args) {
        printParsingTable();

        String input = "id + id * id $";
        String[] tokens = input.split(" ");

        Stack<Integer> stateStack = new Stack<>();
        stateStack.push(0);

        int i = 0;

        while (true) {
            int state = stateStack.peek();
            String token = tokens[i];

            String act = action[state][colMap.get(token)];

            if (act == null || act.equals("")) {
                System.out.println(" Rejected");
                return;
            }

            if (act.equals("acc")) {
                System.out.println(" Accepted");
                return;
            }

            if (act.startsWith("s")) {
                int nextState = Integer.parseInt(act.substring(1));
                stateStack.push(nextState);
                i++;
            }

            else if (act.startsWith("r")) {
                int prodIndex = Integer.parseInt(act.substring(1));
                String prod = productions[prodIndex];

                String rhs = prod.split("->")[1];
                int popCount = rhs.equals("id") ? 1 : rhs.length();

                for (int j = 0; j < popCount; j++) {
                    stateStack.pop();
                }

                int top = stateStack.peek();
                char lhs = prod.charAt(0);

                int col = (lhs == 'A') ? 0 : (lhs == 'B') ? 1 : 2;

                int gotoState = goTo[top][col];
                stateStack.push(gotoState);
            }
        }
    }
}