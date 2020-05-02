package screenshot;

import java.nio.file.Path;

public interface IScreenshot {

    boolean init();

    boolean take();

    Path get();
}
