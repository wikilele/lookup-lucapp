package model;

import java.awt.image.BufferedImage;

import lombok.Getter;

public class Answer extends QuizEntity{
    @Getter
    private final int number;
    private int score;

    public Answer(int num, BufferedImage img){
        super(img);
        this.number = num;
        this.score = 0;
    }
}
