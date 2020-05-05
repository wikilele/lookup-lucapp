package model;

import java.awt.image.BufferedImage;

import lombok.Getter;
import lombok.Setter;

public class Answer extends QuizEntity{
    @Getter
    private final int number;
    @Getter
    private int score;

    public Answer(int num, BufferedImage img){
        super(img);
        this.number = num;
        this.score = 0;
    }

    public void setScore(int score, Question q) {
        this.score = score;
        if (q.isNegative())
            this.score = -score;
    }
}
