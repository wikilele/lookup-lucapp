package gui;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

import bot.LiveQuizBot;
import model.Answer;
import model.Question;

public class LookupLucapp {
    private JPanel lookupLucappPanel;
    private JPanel quizPanel;
    private JPanel questionPanel;
    private JPanel answersPanel;
    private JPanel timePanel;
    private JButton screenshotButton;
    private JLabel questionLabel;
    private JLabel timeLabel;
    private JPanel answer3Panel;
    private JPanel answer2Panel;
    private JPanel answer1Panel;
    private JLabel answer3ScoreLabel;
    private JLabel answer3Label;
    private JLabel answer2ScoreLabel;
    private JLabel answer2Label;
    private JLabel answer1ScoreLabel;
    private JLabel answer1Label;
    private LiveQuizBot liveQuizBot;

    private static Color LIGHT_YELLOW = new Color(255,255,102);
    private static Color LIGHT_GREEN = new Color(144,238,144);
    private static Color LIGHT_RED = new Color(255,100,100);

    public LookupLucapp() {
        liveQuizBot = new LiveQuizBot();
        screenshotButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                long time = 0;
                try {
                    time = liveQuizBot.solve();
                } catch (Exception e) {
                    JOptionPane.showMessageDialog(null,"something went wrong, sorry");
                    return;
                }
                Question question = liveQuizBot.getQuestion();
                List<Answer> answers = liveQuizBot.getAnswers();

                questionLabel.setText(question.getOriginalText());

                int maxScore = Integer.MIN_VALUE;
                int minScore = Integer.MAX_VALUE;

                for (Answer a : answers) {
                    int score = a.getScore();
                    if (score > maxScore) maxScore = score;
                    if (score < minScore) minScore = score;
                }

                for (int i = 0; i < answersPanel.getComponents().length; i ++) {
                    JPanel answerPanel = (JPanel) answersPanel.getComponent(i);
                    JLabel answerLabel = (JLabel) answerPanel.getComponent(0);
                    JLabel answerScoreLabel = (JLabel) answerPanel.getComponent(1);

                    int score = answers.get(i).getScore();
                    answerLabel.setText(answers.get(i).getOriginalText());
                    answerScoreLabel.setText(String.valueOf(score));

                    Color backgroundColor = LIGHT_YELLOW;
                    if (score == maxScore) {
                        backgroundColor = LIGHT_GREEN;
                    } else if (score == minScore) {
                        backgroundColor = LIGHT_RED;
                    }
                    answerPanel.setBackground(backgroundColor);
                }
                timeLabel.setText(time/1000.0 + " seconds");
            }
        });
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Lookup Lucapp");
        LookupLucapp lookupLucapp = new LookupLucapp();

        frame.setContentPane(lookupLucapp.lookupLucappPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);

        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int screenHeight = screenSize.height;
        int screenWidth = screenSize.width;
        frame.setSize(screenWidth/2,screenHeight/2);
        frame.setLocation(screenWidth/3,screenHeight/5);

    }

}
