/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import imagetotext.ImageParser;
import imagetotext.TesseractOCR;
import model.Answer;

public class LookupLucapp {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        ImageParser imageParser;
        TesseractOCR ocr = new TesseractOCR();
        Path screenPath = Paths.get("src","test","resources","screens","livequiz0.jpg");
        try {
            imageParser = new ImageParser(screenPath);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        ocr.apply(imageParser.getQuestion().getImage());

        for(Answer a: imageParser.getAnswers()){
            ocr.apply(a.getImage());
        }
    }
}
