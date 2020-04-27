/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import imagetotext.Screenshot;

public class LookupLucapp {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        Path screenPath = Paths.get("src","test","resources","screens","livequiz2.jpg");
        try {
            Screenshot screenshot = new Screenshot(screenPath);

        } catch (IOException e) {
            e.printStackTrace();
        }


    }
    
}
