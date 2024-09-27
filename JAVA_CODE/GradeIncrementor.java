import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class GradeIncrementor 
{
    public static void main(String[] args) 
    {
        String input = "grades.txt";
        String output = "results.txt";

        List<Integer> grades = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(input))) 
        {
            String line;
            while ((line = reader.readLine()) != null) 
            {
                int grade = Integer.parseInt(line.trim());
                grades.add(grade);
            }
        } 
        catch (IOException e) 
        {
            System.out.println("ERROR READING FILE : " + e.getMessage());
        }

        List<Integer> incrementedGrades = new ArrayList<>();
        for (int grade : grades) 
        {
            if (grade < 10) 
            {
                incrementedGrades.add(grade + 1);
            } 
            else 
            {
                incrementedGrades.add(grade);
            }
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(output))) 
        {
            for (int grade : incrementedGrades) 
            {
                writer.write(Integer.toString(grade));
                writer.newLine();
            }
        } 
        catch (IOException e) 
        {
            System.out.println("ERROR WRITING FILE : " + e.getMessage());
        }

        System.out.println("INCREMENTED GRADES FROM results.txt :");
        try (BufferedReader reader = new BufferedReader(new FileReader(output))) 
        {
            String line;
            while ((line = reader.readLine()) != null) 
            {
                System.out.println(line);
            }
        } 
        catch (IOException e) 
        {
            System.out.println("ERROR READING FILE : " + e.getMessage());
        }
    }
}