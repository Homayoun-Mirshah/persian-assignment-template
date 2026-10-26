import java.util.List;

public final class Statistics {
    private Statistics() { }

    // Compute the mean of a non-empty list.
    public static double mean(List<Double> values) {
        if (values.isEmpty()) {
            throw new IllegalArgumentException("Empty input");
        }
        double sum = 0.0;
        for (double value : values) {
            sum += value;
        }
        return sum / values.size();
    }

    @SuppressWarnings("unused")
    public static void main(String[] args) {
        System.out.println(mean(List.of(2.0, 4.0, 6.0)));
    }
}
