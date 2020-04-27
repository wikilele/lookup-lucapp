package search;

public class TextProcessing {
    public static String cleanSpaces(String text) {
        return text.replace("\n", " ")
                .replace("\r", " ")
                .trim();
    }
}
