package imagetotext;

import java.awt.image.BufferedImage;
import java.io.File;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.Paths;

import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;

public class TesseractOCR {

    public void apply(BufferedImage image){
        Tesseract tesseract = new Tesseract();
        try {
            Path tessdataPath = Paths.get("src","main","resources","tessdata");
            tesseract.setLanguage("ita");
            tesseract.setDatapath(tessdataPath.toString());

            /*
             * HACK: set env variable LC_NUMERIC=C
             */
            String text = tesseract.doOCR(image);

            // path of your image file
            System.out.print(text);
        }
        catch (TesseractException e) {
            e.printStackTrace();
        }
    }

    public String getQuestion(){
        return "question";
    }


    public String getOption(int optionIndex){
        return "option" + optionIndex;
    }
}
