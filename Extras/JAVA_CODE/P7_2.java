/*
Let's create a program that generates a randomly ordered deck of cards using Java. 
The program should create a deck of cards, shuffle the order of the cards, and then
display the cards in random order to the user. We'll use ArrayList to store the 
deck of cards and methods such as shuffle() and random() to randomize the order 
of the cards.
• Create a class called Card with fields suit and rank.
• Create a class called Deck with an ArrayList object of Card type, called cards, and methods such as 
shuffle() and displayCards().
• Add 52 cards with 4 different suits, aces, numbers, and face cards.
• Use the shuffle() method of the Collections class in Java to shuffle the 
deck of cards.
• Finally, display the cards using the displayCards() method

*/

import java.util.ArrayList;
import java.util.Collections;

class Card 
{
    String suit;
    String rank;

    public Card(String suit, String rank) 
    {
        this.suit = suit;
        this.rank = rank;
    }

    @Override
    public String toString() 
    {
        return rank + " of " + suit;
    }
}

class Deck 
{
    ArrayList<Card> cards;

    public Deck() 
    {
        this.cards = new ArrayList<>();
        String[] suits = {"HEARTS", "DIAMONDS", "CLUBS", "SPADES"};
        String[] ranks = {"ACE", "2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING"};

        for (String suit : suits) 
        {
            for (String rank : ranks) 
            {
                cards.add(new Card(suit, rank));
            }
        }
    }

    public void shuffle() 
    {
        Collections.shuffle(cards);
    }

    public void displayCards() 
    {
        for (Card card : cards) 
        {
            System.out.println(card);
        }
    }
}

public class P7_2 
{
    public static void main(String[] args) 
    {
        Deck deck = new Deck();
        deck.shuffle();
        deck.displayCards();
    }
}
