/*public class Word_Counter {
    
}gh
*/

import java.util.*;
import java.util.stream.Collectors;

public class Word_Counter 
{
    private String originalText;
    private Map<String, Integer> wordFrequency;
    private int totalWords;

    public void analyzeText(String text) 
    {
        this.originalText = text;
        String[] words = text.toLowerCase().replaceAll("[^a-z0-9\\s]", "").split("\\s+");

        this.wordFrequency = new HashMap<>();
        for (String word : words) 
        {
            if (!word.isEmpty()) 
            {
                wordFrequency.put(word, wordFrequency.getOrDefault(word, 0) + 1);
            }
        }
        this.totalWords = words.length;
    }
    public Map<String, Integer> getWordFrequency() 
    {
        return new HashMap<>(wordFrequency);
    }

    public String getMostFrequentWord() 
    {
        return wordFrequency.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse("");
    }
    
    public List<String> getLeastFrequentWords(int n) 
    {
        return wordFrequency.entrySet().stream()
                .sorted(Map.Entry.comparingByValue())
                .limit(n)
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
    }
/*
    public String replaceWord(String oldWord, String newWord) 
    {
        String newText = originalText.replaceAll("(?i)\\b" + oldWord + "\\b", newWord);
        analyzeText(newText);
        return newText;
    }
*/
    public String removeWord(String word) 
    {
        String newText = originalText.replaceAll("(?i)\\b" + word + "\\b", "").replaceAll("\\s+", " ").trim();
        analyzeText(newText);
        return newText;
    }

    public String getCurrentText() 
    {
        return originalText;
    }

    public int getTotalWords() 
    {
        return totalWords;
    }


    public static void main(String[] args) 
    {
        Word_Counter scan = new Word_Counter();
        Scanner sc = new Scanner(System.in);

        System.out.println("ENTER TEXT TO ANALYZE : ");
        String text = sc.nextLine();
        scan.analyzeText(text);

        String[] words = text.split(" ");
        int wordCount = words.length;
        System.out.println("TOTAL WORDS : " + wordCount);
       
        System.out.println("ANALYSIS COMPLETE.");
        while (true) 
        {
            System.out.println("\nWORD ANALYZER MENU:");
           
            System.out.println("1. GET WORD FREQUENCY.");
            System.out.println("2. GET MOST FREQUENT WORD.");
            System.out.println("3. GET LEAST FREQUENT WORDS.");
            System.out.println("4. REPLACE WORD.");
            System.out.println("5. REMOVE WORD.");
            System.out.println("6. PRINT CURRENT TEXT.");
            System.out.println("7. EXIT.");
           
            System.out.print("\nENTER YOUR CHOICE : ");
                int choice = sc.nextInt();
                sc.nextLine();
                switch (choice) 
                {
                case 1:
                try 
                {
                    Map<String, Integer> frequency = scan.getWordFrequency();
                    for (Map.Entry<String, Integer> entry : frequency.entrySet()) 
                    {
                        System.out.println(entry.getKey() + " : " + entry.getValue());
                    }
                    break;
                } 
                catch (Exception e) 
                {
                     System.out.println("ENTER AN INPUT FIRST.");
                }
                 
                case 2:
                    String mostFrequent = scan.getMostFrequentWord();
                    System.out.println("MOST FREQUENT WORD: " + mostFrequent);
                    break;
                case 3:
                    System.out.println("ENTER THE NUMBER OF LEAST FREQUENT WORDS TO DISPLAY : ");
                    int n = sc.nextInt();
                    sc.nextLine(); 
                    List<String> leastFrequent = scan.getLeastFrequentWords(n);
                    System.out.println("LEAST FREQUENT WORDS : " + String.join(", ", leastFrequent));
                    break;
                case 4:
                    System.out.print("ENTER THE WORD TO REPLACE: ");
                    String wordToReplace = sc.nextLine();
                    System.out.print("ENTER THE NEW WORD: ");
                    String newWord = sc.nextLine();
                    boolean wordFound = false;
                for (int i = 0; i < words.length; i++) 
                {
                    if (words[i].equals(wordToReplace)) 
                    {
                        words[i] = newWord;
                        wordFound = true;
                        break;
                    }
                }
                if (!wordFound) 
                {
                    System.out.println("ERROR : WORD NOT FOUND IN ORIGINAL TEXT.");
                } 
                else 
                {
                    String updatedText = String.join(" ", words);
                    System.out.println("UPDATED TEXT: " + updatedText);
                }
                break;
                
                case 5:
                    System.out.println("ENTER THE WORD TO REMOVE : ");
                    String wordToRemove = sc.nextLine();
                    String removedText = scan.removeWord(wordToRemove);
                    System.out.println("UPDATED TEXT : " + removedText);
                    System.out.println("TOTAL WORDS : " + scan.getTotalWords());
                    break;
                case 6:
                    System.out.println("CURRENT TEXT : " + scan.getCurrentText());
                    break;
                case 7:
                    System.out.println("EXITING...");
                    sc.close();
                    System.exit(0);
    
                default:
                    System.out.println("INVALID CHOICE. PLEASE TRY AGAIN.");
            }
        }
    }
}