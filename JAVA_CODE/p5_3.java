


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class p5_3 {
    public static void main(String[] args) 
    {   
        Path documentsDir = Paths.get("Documents");
        try 
        {
            Files.createDirectory(documentsDir);
        } 
        catch (IOException e) 
        {
            System.err.println("ERROR CREATING DOCUMENTS DIRECTORY : " + e.getMessage());
        }
        Path workDir = documentsDir.resolve("WORK");
        try 
        {
            Files.createDirectory(workDir);
        } 
        catch (IOException e) 
        {
            System.err.println("ERROR CREATING WORK DIRECTORY : " + e.getMessage());
        }
        try 
        {
            Files.createFile(workDir.resolve("project1.txt"));
            Files.createFile(workDir.resolve("project2.txt"));
        } 
        catch (IOException e) 
        {
            System.err.println("ERROR CREATING PROJECT FILES : " + e.getMessage());
        }
        Path personalDir = documentsDir.resolve("Personal");
        try 
        {
            Files.createDirectory(personalDir);
        } 
        catch (IOException e) 
        {
            System.err.println("ERROR CREATING PERSONAL DIRECTORY : " + e.getMessage());
        }
        try 
        {
            Files.createFile(personalDir.resolve("weekendPlan.txt"));
            Files.createFile(personalDir.resolve("summerTrip.txt"));
        } 
        catch (IOException e) 
        {
            System.err.println("ERROR CREATING PERSONAL FILES : " + e.getMessage());
        }
    }
}