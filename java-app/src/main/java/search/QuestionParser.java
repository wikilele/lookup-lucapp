package search;

public class QuestionParser {
    private final String originalQuestion;
    private String simplifiedQuestion;
    private boolean isNegative;

    QuestionParser(String question){
        originalQuestion = question;
    }

    public boolean isNegative(){
        return isNegative;
    }

    public String simplifyQuestion(){
        return simplifiedQuestion;
    }

}
