/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import imagetotext.ImageParser;
import imagetotext.TesseractOCR;
import model.Answer;
import model.Question;
import search.GoogleSearch;
import text.TextProcessing;
import util.Time;

public class LookupLucapp {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Path screenPath = Paths.get("src","test","resources","screens","livequiz2.jpg");
        ImageParser imageParser;
        TesseractOCR ocr = new TesseractOCR();
        GoogleSearch googleSearch = new GoogleSearch();

        Time mainTime = new Time("main");
        try {
            imageParser = new ImageParser(screenPath);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        Time questionTime = new Time("question");
        Question question = imageParser.getQuestion();

        ocr.apply(question);
        TextProcessing.deletePunctuation(question);
        TextProcessing.deleteStopWords(question);

        questionTime.end();

        List<Answer> answers = imageParser.getAnswers();
        List<BotThread> botThreads = new ArrayList<>();

        Time answersTime = new Time("answers") ;
        for(Answer a: answers){
            BotThread botThread = new BotThread(question,a);
            botThreads.add(botThread);
            botThread.start();
        }

        for(BotThread botThread : botThreads) {
            try {
                botThread.join();
            } catch (InterruptedException e) {
                continue;
            }
        }
        answersTime.end();

        System.out.println(question.getOriginalText());
        System.out.println(answers.get(0).getOriginalText() + " score: " + answers.get(0).getScore());
        System.out.println(answers.get(1).getOriginalText() + " score: " + answers.get(1).getScore());
        System.out.println(answers.get(2).getOriginalText() + " score: " + answers.get(2).getScore());

        mainTime.end();
    }
}
