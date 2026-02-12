import java.util.*;

public class CanJumpTest {
    public boolean canJump(int[] arr) {
        if (arr == null) return false;
        if (arr.length < 2) return true; // empty or single-element array -> true
        boolean[] visited = new boolean[arr.length];
        return helper(arr, 0, visited);
    }

    private boolean helper(int[] arr, int idx, boolean[] visited) {
        // invalid index
        if (idx < 0 || idx >= arr.length) return false;
        // reached last index
        if (idx == arr.length - 1) return true;
        // already visited this index -> avoid cycles
        if (visited[idx]) return false;

        visited[idx] = true;
        int step = arr[idx];
        // can't move anywhere
        if (step == 0) return false;

        // try left
        if (helper(arr, idx - step, visited)) return true;
        // try right
        if (helper(arr, idx + step, visited)) return true;

        return false;
    }

    // small test harness
    public static void main(String[] args) {
        CanJumpTest solver = new CanJumpTest();
        int[][] tests = new int[][]{
            {3,1,2,2,5}, // expected true
            {1},         // true
            new int[] {},// true (empty)
            {0},         // true (single element)
            {2,0,0,0,0}, // false
            {1,2,3},     // true? let's see
            {4,1,2,3,0,0} // depends
        };

        for (int[] t : tests) {
            System.out.println(Arrays.toString(t) + " -> " + solver.canJump(t));
        }
    }
}
