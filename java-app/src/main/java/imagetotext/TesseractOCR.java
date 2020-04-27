package imagetotext;

import java.awt.image.BufferedImage;
import java.nio.file.Path;
import java.nio.file.Paths;

import model.QuizEntity;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;
import search.TextProcessing;

public class TesseractOCR {
    private Tesseract tesseract;

    public TesseractOCR() {
        tesseract = new Tesseract();

        Path tessdataPath = Paths.get("src","main","resources","tessdata");
        tesseract.setLanguage("ita");
        tesseract.setDatapath(tessdataPath.toString());
    }

    public String apply(BufferedImage image){
        try {
            /*
             * HACK: set env variable LC_NUMERIC=C
             */
            String text = tesseract.doOCR(image);

            return TextProcessing.cleanSpaces(text);
        }
        catch (TesseractException e) {
            e.printStackTrace();
            return "";
        }
    }

    public void apply(QuizEntity entity){
        String text = this.apply(entity.getImage());
        entity.setText(text);
    }
}
