/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lookup.lucapp;

/**
 *
 * @author leonardo
 */
public class AdbSmartphone implements ISmartphone {
    private final String imgPath = "Screens/screen.png";
    
    public boolean connect(){
        return true;
    }
        

    public String takeScreenshot(){
        return imgPath;
    }

}
