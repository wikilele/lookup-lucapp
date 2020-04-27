package model;

import java.awt.image.BufferedImage;

import lombok.Getter;
import lombok.Setter;

public abstract class QuizEntity {

    @Getter
    @Setter
    private BufferedImage image;
    @Getter
    @Setter
    private String text;

    public QuizEntity(BufferedImage img){
        this.image = img;
        this.text = "";
    }
}
