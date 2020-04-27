package screenshot;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

public class AdbScreenshot implements IScreenshot {
    String imgPath = "resources/screen.png";

    private void execBashCommand(String... command) throws IOException, InterruptedException{
        ArrayList<String> commandString = new ArrayList<String>(command.length);
        commandString.addAll(Arrays.asList(command));

        ProcessBuilder pb = new ProcessBuilder();
        pb.command(commandString);
        pb.inheritIO();
        Process process = pb.start();
        process.waitFor();
    }

    @Override
    public boolean init(){
        try{
            execBashCommand( "adb", "devices");
        } catch (InterruptedException | IOException e){
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @Override
    public boolean take(){

        try {
            execBashCommand("/bin/bash","-l", "-c", "adb exec-out screencap -p >" + imgPath);
        } catch (InterruptedException | IOException e){
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @Override
    public String getAsString(){
        return imgPath;
    }

}
