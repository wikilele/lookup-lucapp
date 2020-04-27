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

import lombok.Getter;
public class Screenshot {
    private final int HEIGHT;
    private final int WIDTH;

    private final int TOP;
    private final int BOTTOM;

    private BufferedImage original;
    private BufferedImage toProcess;
    @Getter
    private BufferedImage question;
    @Getter
    private ArrayList<BufferedImage> answers = new ArrayList<>();

    private ArrayList<Integer> HEIGHT_SCOPES = new ArrayList<>();

    public Screenshot(Path imgPath) throws  IOException{
        original = ImageIO.read(imgPath.toFile());
        HEIGHT = original.getHeight();
        WIDTH = original.getWidth();
        TOP = HEIGHT * 25/100;
        BOTTOM = HEIGHT - HEIGHT*15/100;

        toBlackAndWhite();
        print(toProcess);
        System.out.println(HEIGHT);
        System.out.println(WIDTH);
        findAnswersSpots();
        // now we get the question and the answer sub images
        split();
    }



    private void toBlackAndWhite() {
        toProcess = new BufferedImage(WIDTH,HEIGHT,BufferedImage.TYPE_BYTE_BINARY);
        Graphics2D g2d = toProcess.createGraphics();
        g2d.drawImage(original, 0, 0, Color.WHITE,null);
        g2d.dispose();
    }

    private void findAnswersSpots(){

        int y = BOTTOM;
        boolean wasWhite = false;
        while (y > TOP && HEIGHT_SCOPES.size() < 6){
            int blackCount = 0;
            int whiteCount = 0;
            for(int x = 0; x < WIDTH; x ++){
                int pixelColor = toProcess.getRGB(x,y);
                if (pixelColor == Color.WHITE.getRGB()) whiteCount ++;
                if (pixelColor == Color.BLACK.getRGB()) blackCount ++;
            }

            if (whiteCount > blackCount && !wasWhite){
                // we are in the answer section
                // we just entered this section so we need to record this y
                System.out.println("from");
                System.out.println(y);
                HEIGHT_SCOPES.add(y);

                wasWhite = true;
            }
            if (blackCount > whiteCount && wasWhite){
                // we are in a non answer section
                // we just exited the answer section so we need to record this y
                System.out.println("to");
                System.out.println(y);
                HEIGHT_SCOPES.add(y);

                wasWhite = false;
            }

            y = y - 1; // in this way it's a bit faster but still correct
        }
        Collections.reverse(HEIGHT_SCOPES);
    }

    public void split() {
        question = this.toProcess.getSubimage( 0, TOP, WIDTH, HEIGHT_SCOPES.get(0) - TOP);
        print(question);

        int from = HEIGHT_SCOPES.get(0);
        int to = HEIGHT_SCOPES.get(1);

        answers.add(this.toProcess.getSubimage( 0, from, WIDTH, to - from));
        print(answers.get(0));

        from = HEIGHT_SCOPES.get(2);
        to = HEIGHT_SCOPES.get(3);

        answers.add(this.toProcess.getSubimage( 0, from, WIDTH, to - from));
        print(answers.get(1));

        from = HEIGHT_SCOPES.get(4);
        to = HEIGHT_SCOPES.get(5);

        answers.add(this.toProcess.getSubimage( 0, from, WIDTH, to - from));
        print(answers.get(2));

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
