package model;

import java.awt.image.BufferedImage;

import lombok.Getter;
import lombok.Setter;

public abstract class QuizEntity {

    @Getter
    @Setter
    private BufferedImage image;
    @Getter
    private String originalText;
    @Getter
    @Setter
    private String processedText;

    public QuizEntity(BufferedImage img){
        this.image = img;
        this.originalText = null;
        this.processedText = null;
    }

    public void initOriginalText(String originalText) {
        if (this.originalText == null) {
            this.originalText = originalText;
            this.processedText = originalText;
        }
    }
}
