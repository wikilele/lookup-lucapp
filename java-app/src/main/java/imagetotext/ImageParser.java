package imagetotext;

import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Graphics2D;
import java.io.IOException;
import java.awt.image.BufferedImage;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import model.Answer;
import model.Question;

public class ImageParser {
    private final int HEIGHT;
    private final int WIDTH;

    // this points define a rectangle were the questions and the answers are located
    private final int TOP;
    private final int BOTTOM;
    private final int LEFT;
    private final int RIGHT;

    private final int WHITE = Color.WHITE.getRGB();
    private final int BLACK = Color.BLACK.getRGB();

    private final BufferedImage original;

    private BufferedImage question;
    private ArrayList<BufferedImage> answers = new ArrayList<>();

    public ImageParser(Path imgPath) throws  IOException{
        original = ImageIO.read(imgPath.toFile());
        HEIGHT = original.getHeight();
        WIDTH = original.getWidth();
        // the percentage values are set empirically
        TOP = HEIGHT * 25/100;
        BOTTOM = HEIGHT - HEIGHT*15/100;
        LEFT = WIDTH * 8/100;
        RIGHT = WIDTH - LEFT;

        process(original);
    }

    private void process(BufferedImage screenshot){
        BufferedImage screenshotBlackAndWhite =  toBlackAndWhite(screenshot);
        ArrayList<Integer> HEIGHT_SCOPES = findAnswersSpots(screenshotBlackAndWhite);

        colorBorderWhite(screenshotBlackAndWhite, LEFT,RIGHT, HEIGHT_SCOPES.get(0),HEIGHT_SCOPES.get(5));

        // now we get the question and the answer sub images
        split(screenshotBlackAndWhite,HEIGHT_SCOPES);

        colorSwap(question);
        //print(question);
        //print(answers.get(0));
        //print(answers.get(1));
        //print(answers.get(2));
    }

    /**
     * the image is converted to black and white because it's easier to find elements in it
     * and the OCR will perform better
     */
    private BufferedImage toBlackAndWhite(BufferedImage colored) {
        BufferedImage blackAndWhite = new BufferedImage(colored.getWidth(),colored.getHeight(),BufferedImage.TYPE_BYTE_BINARY);
        Graphics2D g2d = blackAndWhite.createGraphics();
        g2d.drawImage(colored, 0, 0, Color.WHITE,null);
        g2d.dispose();

        return blackAndWhite;
    }

    /**
     * it search for the spots where the answers are placed
     * each answer is surrounded by a white balloon
     *
     * the function searches, bottom up, for the first line where the white pixels are greater than the black ones
     * this means that it is the beginning of the answer balloon
     * then it searches for the first line where black pixels are greater than white ones
     * this means the answer balloon has ended
     */
    private ArrayList<Integer> findAnswersSpots(BufferedImage image){
        ArrayList<Integer> HEIGHT_SCOPES = new ArrayList<>();
        // the step used in the while loop, greater the step faster the scanning but it may become not correct
        // one ot two (even three) should be a good value
        int STEP = 2;

        int y = BOTTOM;
        boolean wasWhite = false;
        while (y > TOP && HEIGHT_SCOPES.size() < 6){
            int blackCount = 0;
            int whiteCount = 0;
            for(int x = 0; x < WIDTH; x ++){
                int pixelColor = image.getRGB(x,y);
                if (pixelColor == Color.WHITE.getRGB()) whiteCount ++;
                if (pixelColor == Color.BLACK.getRGB()) blackCount ++;
            }

            if (whiteCount > blackCount && !wasWhite){
                // we are in the answer section
                // we just entered this section so we need to record this y
                HEIGHT_SCOPES.add(y);

                wasWhite = true;
            }
            if (blackCount > whiteCount && wasWhite){
                // we are in a non answer section
                // we just exited the answer section so we need to record this y
                // y - 1 because we don't want the black line
                HEIGHT_SCOPES.add(y + 1);

                wasWhite = false;
            }

            y = y - STEP;
        }
        Collections.reverse(HEIGHT_SCOPES);

        return HEIGHT_SCOPES;
    }

    /**
     * According to the scopes founded we split the image getting the question and the answers
     */
    private void split(BufferedImage image, ArrayList<Integer> HEIGHT_SCOPES) {
        question = image.getSubimage( 0, TOP, WIDTH, HEIGHT_SCOPES.get(0) - TOP);

        for(int i = 0; i < HEIGHT_SCOPES.size(); i = i + 2){
            int from = HEIGHT_SCOPES.get(i);
            int to = HEIGHT_SCOPES.get(i + 1);

            answers.add(image.getSubimage( LEFT, from, RIGHT - LEFT, to - from));
        }
    }

    /**
     * the answers still have a bit of non white borders, we want to delete that
     * in order to improve OCR
     *
     * the coordinates in input refer to the rectangle containing the answers
     */
    private void colorBorderWhite(BufferedImage image, int fromX, int toX, int fromY, int toY){
        for (int y = fromY; y < toY; y++){
            // if the first pixel is black it's ok the color all the line white
            if (image.getRGB(fromX,y) != WHITE){
                for(int x = fromX; x < toX; x ++){
                    image.setRGB(x,y,WHITE);
                }
            }
        }
    }


    /**
     * swaps the color of an image, it's useful for the question in order to have the words in black
     */
    private void colorSwap(BufferedImage image){
        int black = Color.BLACK.getRGB();
        int white = Color.WHITE.getRGB();
        for(int x = 0; x < image.getWidth(); x ++){
            for(int y = 0; y < image.getHeight(); y++){
                int pixelColor = image.getRGB(x,y);
                if(pixelColor == white) image.setRGB(x,y,black);
                if(pixelColor == black) image.setRGB(x,y,white);
            }
        }
    }

    public Question getQuestion(){
        return new Question(question);
    }

    public ArrayList<Answer> getAnswers(){
        ArrayList<Answer> retvalue = new ArrayList<>();
        for(int i = 0; i < answers.size(); i ++){
            retvalue.add(new Answer(i,answers.get(i)));
        }
        return  retvalue;
    }


    private void print(BufferedImage img) {
        ImageIcon icon=new ImageIcon(img);
        JFrame frame=new JFrame();
        frame.setLayout(new FlowLayout());
        frame.setSize(img.getWidth(),img.getHeight());
        JLabel lbl=new JLabel();
        lbl.setIcon(icon);
        frame.add(lbl);
        frame.setVisible(true);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

}
