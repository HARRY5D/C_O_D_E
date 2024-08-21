import harmonic.*;
import java.util.*;

public class p3_4 
{
    public static void main(String[] args) 
    {

        Scanner sc = new Scanner(System.in);
        System.out.print("ENTER No. OF TERMS : ");
        int n = sc.nextInt();

        Harmonic hc = new Harmonic();
        double sum = hc.calculate(n);

        System.out.println("THE SUM OF HARMONIC SERIES UPTO " + n + " TERMS IS : " + sum);
    }

}