package bot;

import imagetotext.TesseractOCR;
import model.Answer;
import model.Question;
import search.GoogleSearch;
import text.TextProcessing;

public class BotThread  extends Thread {

    private final Question question;
    private final Answer answer;

    public BotThread(Question question, Answer answer) {
        this.question = question;
        this.answer = answer;
    }

    @Override
    public void run() {
        TesseractOCR ocr = new TesseractOCR();
        GoogleSearch googleSearch = new GoogleSearch();

        ocr.apply(answer);
        TextProcessing.deletePunctuation(answer);
        TextProcessing.deleteStopWords(answer);

        googleSearch.search(question,answer);
    }
}
