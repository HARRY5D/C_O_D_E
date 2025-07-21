import java.io.*;

public class stream 
{
    public static void main(String[] args) 
    {
        try 
        {
            FileInputStream fis = new FileInputStream("fi.txt");
            FileOutputStream fos = new FileOutputStream("fio.txt");

            int c;

            while ( (c=fis.read())!= -1) 
            { 
                fos.write(c);
                System.out.println(c);
            }
            fis.close();
            fos.close();

        } 
        catch (Exception e) 
        {
            System.out.println(e);
            e.printStackTrace();
        }    
    }
}
