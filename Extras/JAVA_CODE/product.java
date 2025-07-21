import java.util.Scanner;

class product {
   
    float  productNo;
    String productName;
    String activationKey;
    float priceofProduct;

    Scanner sc = new Scanner(System.in);
   
    String getProductName() 
    {
        System.out.print("ENTER PRODUCT NAME : ");
        productName = sc.nextLine();
        return productName;
    }
 
    String getActivationKey() 
    {
        System.out.print("ENTER PRODUCT ACTIVATION KEY : ");    
        activationKey = sc.nextLine();
        return activationKey;
    }

    float getProductNo() 
    {
        System.out.print("ENTER PRODUCT No : ");    
        productNo = sc.nextFloat();
        sc.nextLine(); 
        return productNo;
    }

    float getPriceOfProduct() 
    {
        System.out.print("ENTER PRODUCT PRICE : ");    
        priceofProduct = sc.nextFloat();
        sc.nextLine(); 
        return priceofProduct;
    }

    void setActivationKey(String activationKey)
     {
        this.activationKey = activationKey;
    }  

    void display()
     {
        System.out.println("\nYOUR PRODUCT NAME : " + productName);  
        System.out.println("YOUR PRODUCT ACTIVATION KEY : " + activationKey);
        System.out.println("YOUR PRODUCT No : " + productNo);
        System.out.println("YOUR PRODUCT PRICE : " + priceofProduct);
    }
   
    public static void main(String[] args) 
    {
       
        product[] key = new product[5];
         
        for(int i = 0; i < 5; i++) 
        {
            key[i] = new product();
            key[i].getProductName();
            String activationKey = key[i].getActivationKey();
            
            key[i].setActivationKey(activationKey);
            key[i].getProductNo();
            key[i].getPriceOfProduct();
            key[i].display(); // Call display method to print product details
        }
    }
}