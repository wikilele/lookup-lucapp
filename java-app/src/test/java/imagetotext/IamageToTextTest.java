package imagetotext;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;

import model.Answer;
import org.junit.Assert;
import org.junit.Test;

public class IamageToTextTest {
    TesseractOCR ocr = new TesseractOCR();

    @Test
    public void testScreenshot0(){
        String screenshotName = "livequiz0.jpg";
        Screenshot screenshot;

        Path screenPath = Paths.get("src","test","resources","screens",screenshotName);
        try {
            screenshot = new Screenshot(screenPath);
        } catch (IOException e) {
            e.printStackTrace();
            Assert.fail();
            return;
        }

        String questionText = ocr.apply(screenshot.getQuestion().getImage());
        Assert.assertEquals("Quale di questi animali ha un'aspettativa di vita più simile all'uomo?", questionText);

        String[] expectedAnswers = {"Scimpanzé","Coccodrillo","Orca"};
        ArrayList<Answer> answers = screenshot.getAnswers();

        for (int i = 0; i < answers.size(); i++) {
            ocr.apply(answers.get(i));
            Assert.assertEquals(expectedAnswers[i], answers.get(i).getText());
        }
    }
}
