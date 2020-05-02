package model;

import java.awt.image.BufferedImage;

public class Question extends QuizEntity{

    private boolean isNegative = false;

    public Question(BufferedImage img){
        super(img);
    }

    public boolean isNegative() { return isNegative;}
    public void isNegative(boolean n) { isNegative = n;}
}
