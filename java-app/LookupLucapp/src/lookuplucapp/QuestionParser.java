/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lookuplucapp;

/**
 *
 * @author leonardo
 */
public class QuestionParser { //TODO it may implement an interface
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
