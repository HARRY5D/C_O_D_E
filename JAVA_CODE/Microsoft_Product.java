/*
import java.util.Scanner;

class Microsoft_Product 
{
   
    float  productNo;
    String productName;
    String activationKey;
    float priceofProduct;

    
    public Microsoft_Product(float productNo, String productName, String activationKey, float priceofProduct)
     {
        this.productNo = productNo;
        this.productName = productName;
        this.activationKey = activationKey;
        this.priceofProduct = priceofProduct;
    }
    static Scanner sc = new Scanner(System.in);
   
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
   
    public static void Microsoft_Product( String[] args) 
    {
       
        Microsoft_Product[] key = new Microsoft_Product[5];
         
        for(int i = 0; i < 5; i++) 
        {
            key[i] = new MicrosoftProduct(productNo, productName, activationKey, priceofProduct);
        
           // key[i] = new Microsoft_Product();
            key[i].getProductName();
            String activationKey = key[i].getActivationKey();
            
            key[i].setActivationKey(activationKey);
            key[i].getProductNo();
            key[i].getPriceOfProduct();
           
            
        }
       // Microsoft_Product k = new Microsoft_Product;

        System.out.print("Enter product name to search: ");
        String searchProductName = sc.nextLine();
        System.out.print("Enter product number to search: ");
        float searchProductNo = sc.nextFloat();
        
        for (int j = 0; j < 5; j++) {
            
        }
           if (key[j].getProductName().equalsIgnoreCase(searchProductName) && key[i].getProductNo() == searchProductNo) 
           
           {
                key[i].display();
                break;
            }
       /*  for(int i = 0; i < 5; i++) 
        {
            key[i].display();
        }*/




import java.util.Scanner;

public class Microsoft_Product
 {
    private float productNo;
    private String productName;
    private String activationKey;
    private float priceofProduct;

    public Microsoft_Product(float productNo, String productName, String activationKey, float priceofProduct) {
        this.productNo = productNo;
        this.productName = productName;
        this.activationKey = activationKey;
        this.priceofProduct = priceofProduct;
    }

    public String getProductName() {
        return productName;
    }

    public String getActivationKey() {
        return activationKey;
    }

    public float getProductNo() {
        return productNo;
    }

    public float getPriceofProduct() {
        return priceofProduct;
    }

    public void setActivationKey(String activationKey) {
        this.activationKey = activationKey;
    }

    public void display() {
        System.out.println("PRODUCT NO: " + productNo);
        System.out.println("PRODUCT NAME: " + productName.toUpperCase());
        System.out.println("ACTIVATION KEY: " + activationKey.toUpperCase());
        System.out.println("PRICE OF PRODUCT: " + priceofProduct);
    }

    public static void main(String[] args) {
        Microsoft_Product[] key = new Microsoft_Product[5];
        Scanner sc = new Scanner(System.in);
        for (int i = 0; i < key.length; i++) {
            System.out.println("ENTER DETAILS FOR PRODUCT " + (i + 1) + ":");
            System.out.print("PRODUCT NO: ");
            float productNo = sc.nextFloat();
            sc.nextLine();
            System.out.print("PRODUCT NAME: ");
            String productName = sc.nextLine();
            System.out.print("ENTER PRODUCT ACTIVATION KEY: ");
            String activationKey = sc.nextLine();
            System.out.print("PRICE OF PRODUCT: ");
            float priceofProduct = sc.nextFloat();
            sc.nextLine();

            key[i] = new Microsoft_Product(productNo, productName, activationKey, priceofProduct);
        }
        System.out.print("ENTER PRODUCT NAME TO SEARCH: ");
        String searchProductName = sc.nextLine();
        System.out.print("ENTER PRODUCT NUMBER TO SEARCH: ");
        float searchProductNo = sc.nextFloat();
        for (Microsoft_Product product : key) 
        
        {
            if (product.getProductName().equalsIgnoreCase(searchProductName) && product.getProductNo() == searchProductNo) {
                product.display();
                break;
            }
        }
        sc.close();
    }
}



