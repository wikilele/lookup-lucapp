package bot;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

import imagetotext.ImageParser;
import imagetotext.TesseractOCR;
import lombok.Getter;
import model.Answer;
import model.Question;
import screenshot.AdbScreenshot;
import screenshot.IScreenshot;
import text.TextProcessing;
import util.Time;

public class LiveQuizBot {

    private IScreenshot screenshot;
    private TesseractOCR ocr;
    @Getter
    private Question question;
    @Getter
    private List<Answer> answers;

    public LiveQuizBot() {
        screenshot = new AdbScreenshot();
        screenshot.init();
        ocr = new TesseractOCR();
    }

    public long solve() throws IOException, InterruptedException {
        ImageParser imageParser;

        Time mainTime = new Time("main");

        Time screenshotTime = new Time("screenshot");
        screenshot.take();
        Path screenPath = screenshot.get();
        screenshotTime.end();

        Time questionTime = new Time("question");
        imageParser = new ImageParser(screenPath);
        question = imageParser.getQuestion();
        ocr.apply(question);
        if (TextProcessing.containsNegation(question))
            TextProcessing.deleteNegations(question);
        TextProcessing.deletePunctuation(question);
        TextProcessing.deleteStopWords(question);
        questionTime.end();

        Time answersTime = new Time("answers");
        answers = imageParser.getAnswers();
        List<BotThread> botThreads = new ArrayList<>();
        for(Answer a: answers){
            BotThread botThread = new BotThread(question,a);
            botThreads.add(botThread);
            botThread.start();
        }
        for(BotThread botThread : botThreads) {
            botThread.join();
        }
        answersTime.end();

        return mainTime.end();
    }
}
