import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

class GradeIncrementor 
{
    public static void main(String[] args) 
    {
      

        try (BufferedReader reader = new BufferedReader(new FileReader(grades.txt));BufferedWriter writer = new BufferedWriter(new FileWriter(results.txt))) 
             {

            String line;
            while ((line = reader.readLine()) != null) 
            {
                int grade = Integer.parseInt(line);
                int incrementedGrade;

                if (grade == 10)
                {
                    incrementedGrade = grade;
                }
                else
                {
                    incrementedGrade = grade + 1;
                }
                
                writer.write(String.valueOf(incrementedGrade) + "\n");
                System.out.println("Incremented grade: " + incrementedGrade);
            }

        } 
        catch (IOException e) 
        {
            System.err.println("Error reading or writing file: " + e.getMessage());
        }
    
    }
}
