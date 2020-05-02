package search;

import java.io.IOException;

import org.junit.Assert;
import org.junit.Test;

public class GoogleSearchTest {


    @Test
    public void testSimple() {
        GoogleSearch googleSearch = new GoogleSearch();
        try {
            int value = googleSearch.search("","");
        } catch (IOException e) {
            e.printStackTrace();
            Assert.fail();
        }

    }
}
