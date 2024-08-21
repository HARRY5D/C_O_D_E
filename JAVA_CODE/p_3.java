
abstract class Instrument 
{
    abstract void play();
    abstract String what();
    abstract void adjust();
}

class Wind extends Instrument 
{
    @Override
    void play() 
    {
        System.out.println("WIND INSTRUMENT PLAYED.");
    }
    @Override
    String what() 
    {
        return "WIND";
    }
    @Override
    void adjust() 
    {
        System.out.println("WIND INSTRUMENT TUNED PROPERLY");
    }
}

class Percussion extends Instrument 
{
    @Override
    void play() 
    {
        System.out.println("PERCUSSION INSTRUMENT PLAYED.");
    }
    @Override
    String what() 
    {
        return "PERCUSSION";
    }
    @Override
    void adjust() 
    {
        System.out.println("PERCUSSION INSTRUMENT TUNED PROPERLY.");
    }
}

class Stringed extends Instrument 
{
    @Override
    void play() 
    {
        System.out.println("STRINGED INSTRUMENT PLAYED.");
    }
    @Override
    String what() 
    {
        return "STRINGED";
    }
    @Override
    void adjust() 
    {
        System.out.println("STRINGED INSTRUMENT TUNED PROPERLY.");
    }
}

class Woodwind extends Wind 
{
    @Override
    void play() 
    {
        System.out.println("WOODWIND INSTRUMENT PLAYED.");
    }
    @Override
    String what() 
    {
        return "WOODWIND";
    }
}

class Brass extends Wind 
{
    @Override
    void play() 
    {
        System.out.println("BRASS INSTRUMENT PLAYED.");
    }
    @Override
    void adjust() 
    {
        
        System.out.println("BRASS INSTRUMENT TUNED PROPERLY.");
    }
}

public class p_3 
{
    public static void main(String[] args) 
    {
        
        Wind wind = new Wind();
        
        System.out.println(wind.what());
        wind.play();
        wind.adjust();
        Percussion percussion = new Percussion();
        
        System.out.println(percussion.what());
        percussion.play();
        percussion.adjust();

        Stringed stringed = new Stringed();
        
        System.out.println(stringed.what());
        stringed.play();
        stringed.adjust();
        
        Woodwind woodwind = new Woodwind();
        
        System.out.println(woodwind.what());
        woodwind.play();
        woodwind.adjust();

        Brass brass = new Brass();
        
        System.out.println(brass.what());
        brass.play();
        brass.adjust();

    }
}