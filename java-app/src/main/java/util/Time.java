package util;

public class Time {

    private static String name;
    private static long startTime;

    public static void start(String n) {
        name = n;
        startTime = System.nanoTime();
    }

    public static void end() {
        long duration = (System.nanoTime() - startTime)/1000000;
        System.out.println("TIME:: " + name + " finished in " + (duration) + " milliseconds");
    }
}
