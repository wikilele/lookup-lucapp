/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lookuplucapp;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

/**
 *
 * @author leonardo
 */
public class AdbSmartphone implements ISmartphone {
    private final String imgPath = "Screens/screen.png";
    
    private void execBashCommand(String... command){
        ArrayList<String> commandString = new ArrayList<>(command.length);
        for (String arg : command)
            commandString.add(arg);
        
        ProcessBuilder pb = new ProcessBuilder();
        pb.command(commandString);
        pb.inheritIO();
        try{
            Process process = pb.start();
            process.waitFor();
        }catch (IOException e) {
            e.printStackTrace();
	} catch (InterruptedException e) {
            e.printStackTrace();
	}
        
    }
    
    public boolean connect(){
        execBashCommand( "adb", "devices");
        return true;
    }
        

    public String takeScreenshot(){
 
        execBashCommand("/bin/bash","-l", "-c", "adb exec-out screencap -p >" + imgPath);
        return imgPath;
    }

}
