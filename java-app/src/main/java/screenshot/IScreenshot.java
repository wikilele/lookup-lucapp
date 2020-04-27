package screenshot;

public interface IScreenshot {

    boolean init();

    boolean take();

    String getAsString();
}
