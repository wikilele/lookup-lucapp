package util;

public class Time {

    private final String name;
    private static long startTime;

    public Time(String n) {
        name = n;
        startTime = System.nanoTime();
    }

    public long end() {
        long duration = (System.nanoTime() - startTime)/1000000;
        System.out.println("TIME:: " + name + " finished in " + (duration) + " milliseconds");
        return duration;
    }
}
