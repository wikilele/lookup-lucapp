import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import imagetotext.ImageParser;
import imagetotext.TesseractOCR;
import model.Answer;
import model.Question;
import org.junit.Assert;
import org.junit.Test;
import search.GoogleSearch;
import text.TextProcessing;

public class LookupLucappTest {

    @Test
    public void testQuiz2() {
        Path screenPath = Paths.get("src","test","resources","screens","livequiz2.jpg");
        ImageParser imageParser;
        TesseractOCR ocr = new TesseractOCR();
        GoogleSearch googleSearch = new GoogleSearch();

        try {
            imageParser = new ImageParser(screenPath);
        } catch (IOException e) {
            e.printStackTrace();
            Assert.fail();
            return;
        }

        Question question = imageParser.getQuestion();

        ocr.apply(question);
        TextProcessing.deletePunctuation(question);
        TextProcessing.deleteStopWords(question);

        List<Answer> answers = imageParser.getAnswers();

        for(Answer a: answers){
            ocr.apply(a);

            TextProcessing.deletePunctuation(a);
            TextProcessing.deleteStopWords(a);

            googleSearch.search(question, a);

        }

        System.out.println(answers.get(0).getOriginalText() + " score: " + answers.get(0).getScore());
        System.out.println(answers.get(1).getOriginalText() + " score: " + answers.get(1).getScore());
        System.out.println(answers.get(2).getOriginalText() + " score: " + answers.get(2).getScore());

    }
}
