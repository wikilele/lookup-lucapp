package text;

import org.junit.Assert;
import org.junit.Test;

public class TextProcessingTest {

    @Test
    public void testCoscenzaDiZeno() {

        String question = "Ne \"La coscienza di Zeno\", lo psicanalista del protagonista pubblica le sue memorie per:";

        question = TextProcessing.deletePunctuation(question);
        question = TextProcessing.deleteStopWords(question);

        System.out.println(question);
    }

    @Test
    public  void testIsNegative() {

        String question = "Quale tra queste famiglie NON è presente in";

        Assert.assertTrue(TextProcessing.containsNegation(question));

        question = "Quale tra queste famiglie è presente in";

        Assert.assertFalse(TextProcessing.containsNegation(question));
    }
}
