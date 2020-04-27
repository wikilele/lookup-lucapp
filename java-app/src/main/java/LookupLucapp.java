/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import imagetotext.Screenshot;
import imagetotext.TesseractOCR;

public class LookupLucapp {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Screenshot screenshot;
        TesseractOCR ocr = new TesseractOCR();
        Path screenPath = Paths.get("src","test","resources","screens","livequiz0.jpg");
        try {
            screenshot = new Screenshot(screenPath);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        ocr.apply(screenshot.getQuestion());
        for(BufferedImage a: screenshot.getAnswers()){
            ocr.apply(a);
        }


    }
    
}
