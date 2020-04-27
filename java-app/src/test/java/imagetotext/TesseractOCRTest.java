package imagetotext;

import java.nio.file.Path;
import java.nio.file.Paths;

import org.junit.Test;
public class TesseractOCRTest {

    @Test
    public void simpleTest(){
        TesseractOCR ocr = new TesseractOCR();

        Path resourcePath = Paths.get("src","test","resources","screens","screen.png");
        System.out.println(resourcePath);
        ocr.apply(resourcePath.toString());
    }
}
