package imagetotext;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;

import model.Answer;
import org.junit.Assert;
import org.junit.Test;

public class ImageToTextTest {
    TesseractOCR ocr = new TesseractOCR();

    @Test
    public void testScreenshot0(){
        String expextedQuestion = "Quale di questi animali ha un'aspettativa di vita più simile all'uomo?";
        String[] expectedAnswers = {"Scimpanzé","Coccodrillo","Orca"};
        testScreenshot(0,expextedQuestion,expectedAnswers);
    }

    @Test
    public void testScreenshot1(){
        String expextedQuestion = "Quale di queste app NON esiste?";
        String[] expectedAnswers = {"My Virtual Girlfriend","Snapcat","Snapdog"};
        testScreenshot(1,expextedQuestion,expectedAnswers);
    }

    @Test
    public void testScreenshot2(){
        String expextedQuestion = "In Mr. Robot, come si chiama il temuto hacker che dà a Elliot solo 3 minuti del suo tempo?";
        String[] expectedAnswers = {"Nessuna delle due","Black Lotus","Whiterose"};
        testScreenshot(2,expextedQuestion,expectedAnswers);
    }

    @Test
    public void testScreenshot3(){
        String expextedQuestion = "A quale giornale lavorò Marco Travaglio prima di passare al Fatto Quotidiano?";
        String[] expectedAnswers = {"Il Corriere della Sera","La Stampa","L'Unità"};
        testScreenshot(3,expextedQuestion,expectedAnswers);
    }

    @Test
    public void testScreenshot4(){
        // esponetnte is recognized instead of esponente
        String expextedQuestion = "Sfera Ebbasta è un esponente di quale genere musicale?";
        String[] expectedAnswers = {"Trap","Soul","Musica classica"};
        testScreenshot(4,expextedQuestion,expectedAnswers);
    }

    private void testScreenshot(int number, String expectedQuestion, String[] expectedAnswers){
        String screenshotName = "livequiz" +  Integer.toString(number) + ".jpg";
        ImageParser imageParser;

        Path screenPath = Paths.get("src","test","resources","screens",screenshotName);
        try {
            imageParser = new ImageParser(screenPath);
        } catch (IOException e) {
            e.printStackTrace();
            Assert.fail();
            return;
        }

        String questionText = ocr.apply(imageParser.getQuestion().getImage());
        Assert.assertEquals(expectedQuestion, questionText);


        ArrayList<Answer> answers = imageParser.getAnswers();

        for (int i = 0; i < answers.size(); i++) {
            ocr.apply(answers.get(i));
            Assert.assertEquals(expectedAnswers[i], answers.get(i).getText());
        }
    }
}
