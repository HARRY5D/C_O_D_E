
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class anagram
{
   
    public static List<String> generate(String str)
     {
        List<String> anagrams = new ArrayList<>();

        if (str.length() == 0) 
        {
            anagrams.add("  ");
            return anagrams;
        }

        for (int i = 0; i < str.length(); i++) 
        {
            char current = str.charAt(i);
            String remainingString = str.substring(0, i) + str.substring(i + 1);

            List<String> subAnagrams = generate(remainingString);
            
            for (String sub : subAnagrams) 
            {
                anagrams.add(current + sub);
            }
        }
        return anagrams;
    }

    public static boolean check(String str1, String str2) 
    {
        if (str1.length() != str2.length()) 
        {
            return false;
        }
        
        List<Character> c1 = new ArrayList<>();
        List<Character> c2 = new ArrayList<>();
        
        for (char c : str1.toCharArray()) 
        {
            c1.add(c);
        }
        for (char c : str2.toCharArray()) 
        {
            c2.add(c);
        }
        Collections.sort(c1);
        Collections.sort(c2);
        return c1.equals(c2);
    }
    
    public static void main(String[] args) 
    
    {
        Scanner sc = new Scanner(System.in);
        System.out.print("ENTER STRING : ");
        String originalString = sc.nextLine();

        List<String> anagrams = generate(originalString);
        String randomAnagram = anagrams.get(new Random().nextInt(anagrams.size()));
        System.out.println("RANDOM STRING : " + randomAnagram);

        System.out.print("ENTER YOUR ANAGRAM GUESS: ");
        String userGuess = sc.nextLine();

        if (check(originalString, userGuess)) 
        {
            System.out.println("CORRECT , ITS AN ANAGRAM .");
        }
        else 
        {
            System.out.println("WRONG , THAT'S NOT AN ANAGRAM .");
        }

        sc.close();
    }

}



/*
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class ana {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a string: ");
        String originalString = scanner.nextLine();

        List<String> anagrams = generateAnagrams(originalString);
        String randomAnagram = anagrams.get(new Random().nextInt(anagrams.size()));
        System.out.println("Here's a scrambled version: " + randomAnagram);

        System.out.print("Enter your anagram guess: ");
        String userGuess = scanner.nextLine();

        if (isAnagram(originalString, userGuess)) {
            System.out.println("That's correct! It's an anagram.");
        } else {
            System.out.println("Sorry, that's not an anagram.");
        }

        scanner.close();
    }

    // Generates all possible permutations (anagrams) of a string
    public static List<String> generateAnagrams(String str) {
        List<String> anagrams = new ArrayList<>();
        if (str.length() == 0) {
            anagrams.add("");
            return anagrams;
        }
        for (int i = 0; i < str.length(); i++) {
            char currentChar = str.charAt(i);
            String remainingString = str.substring(0, i) + str.substring(i + 1);
            List<String> subAnagrams = generateAnagrams(remainingString);
            for (String subAnagram : subAnagrams) {
                anagrams.add(currentChar + subAnagram);
            }
        }
        return anagrams;
    }

    // Checks if two strings are anagrams
    public static boolean isAnagram(String str1, String str2) {
        if (str1.length() != str2.length()) {
            return false;
        }
        List<Character> c1 = new ArrayList<>();
        List<Character> c2 = new ArrayList<>();
        for (char c : str1.toCharArray()) {
            c1.add(c);
        }
        for (char c : str2.toCharArray()) {
            c2.add(c);
        }
        Collections.sort(c1);
        Collections.sort(c2);
        return c1.equals(c2);
    }
}

*/