package gui;

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
    private JButton screenshotButton;
    private JLabel questionLabel;
    private JLabel answerOneLabel;
    private JLabel answerTwoLabel;
    private JLabel answerThreeLabel;
    private JLabel timeLabel;
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
                answerOneLabel.setText(answers.get(0).getOriginalText() + " SCORE " + answers.get(0).getScore());
                answerTwoLabel.setText(answers.get(1).getOriginalText() + " SCORE " + answers.get(1).getScore());
                answerThreeLabel.setText(answers.get(2).getOriginalText() + " SCORE " + answers.get(2).getScore());
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

    }

}
