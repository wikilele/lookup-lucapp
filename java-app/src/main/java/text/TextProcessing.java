package text;

import java.io.InputStream;
import java.util.List;
import java.util.Map;

import model.Question;
import model.QuizEntity;
import org.yaml.snakeyaml.Yaml;

public class TextProcessing {

    private static final Map<String, List<String>> toDeleteWords;

    static {
        Yaml yaml = new Yaml();
        InputStream inputStream = TextProcessing.class
                .getClassLoader()
                .getResourceAsStream("to-delete-words.yml");
        toDeleteWords = yaml.load(inputStream);
    }

    public static String cleanSpaces(String text) {
        return text.replace("\n", " ")
                .replace("\r", " ")
                .trim();
    }

    public static String deletePunctuation(String text) {
        return text.replaceAll("\\p{Punct}", "");
    }

    public static String deleteStopWords(String text) {
        text = text.toLowerCase();
        for (String word : toDeleteWords.get("stop_words")) {
            text = text.replaceAll("\\b" + word + "\\b","");
        }
        return text;
    }

    public static boolean containsNegation(String text) {
        List<String> negativeWords = toDeleteWords.get("negative_words");
        boolean isNegative = text.contains(negativeWords.get(0));

        for(String word : negativeWords) {
            isNegative = isNegative || text.contains(word);
        }

        return isNegative;
    }

    public static void deletePunctuation(QuizEntity entity) {
        entity.setProcessedText(deletePunctuation(entity.getProcessedText()));
    }

    public static void deleteStopWords(QuizEntity entity) {
        entity.setProcessedText(deleteStopWords(entity.getProcessedText()));
    }

    public static void containsNegation(Question question) {
        boolean isNegative = containsNegation(question.getOriginalText());
        question.isNegative(isNegative);
    }

}
