package harmonic;

import java.util.*;

public class Harmonic 
{
    public double calculate(int n) 
    {
        double sum = 0.0;
        
        for (int i = 1; i <= n; i++) 
        {
            sum += 1.0 / i;
        }

        return sum;
    }
}

