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
public interface ISmartphone {
    
    public boolean connect();
    /**
     * 
     * @return the path of the screenshot image 
     */
    public String takeScreenshot();
}
