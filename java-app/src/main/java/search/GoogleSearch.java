package search;

import java.io.IOException;
import java.net.URLEncoder;

import model.Answer;
import model.Question;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

// https://stackoverflow.com/questions/3727662/how-can-you-search-google-programmatically-java-api
public class GoogleSearch {
    private final String charset = "UTF-8";
    private final String userAgent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0";
    private final String google =  "http://www.google.com/search?q=";

    public int search(Question question, Answer answer) throws IOException{

        String search = question.getProcessedText() + " " + answer.getProcessedText();
        String url = google + URLEncoder.encode(search, charset);
        Document document = Jsoup.connect(url).userAgent(userAgent).get();

        //System.out.println(document.toString());

        Elements resultStats = document.select("#result-stats");

        String resultsNumber = resultStats.text().split(" ")[1].replace(".","");

        return Integer.parseInt(resultsNumber);
    }
}
