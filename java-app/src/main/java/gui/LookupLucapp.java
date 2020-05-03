package gui;

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

                answer1Label.setText(answers.get(0).getOriginalText());
                answer1ScoreLabel.setText(String.valueOf(answers.get(0).getScore()));

                answer2Label.setText(answers.get(1).getOriginalText());
                answer2ScoreLabel.setText(String.valueOf(answers.get(1).getScore()));
                
                answer3Label.setText(answers.get(2).getOriginalText());
                answer3ScoreLabel.setText(String.valueOf(answers.get(2).getScore()));

                timeLabel.setText(time + " milliseconds");
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
