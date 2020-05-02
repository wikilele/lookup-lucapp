package screenshot;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * adb shell screencap -p | sed 's|\r$||' > screenshot.png
 * /bin/bash","-l", "-c", "adb exec-out screencap -p > screenshot.png
 *
 * */
public class AdbScreenshot implements IScreenshot {
    Path imgPath = Paths.get(System.getProperty("java.io.tmpdir"),"screen.jpg");;

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
            //execBashCommand("/bin/bash","-l", "-c", "adb exec-out screencap -p > " + imgPath);
            execBashCommand("/bin/bash","-l", "-c", "adb shell screencap -p | sed 's|\\r$||' > " + imgPath.toString());
        } catch (InterruptedException | IOException e){
            e.printStackTrace();
            return false;
        }
        return true;
    }

    @Override
    public Path get(){
        return imgPath;
    }

}
