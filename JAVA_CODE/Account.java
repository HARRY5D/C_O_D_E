/*
 Design a class named Account that contains:
 A private int data field named id for the account (default 0).
 A private double data field named balance for the account (default 500₹).
 A private double data field named annualInterestRate that stores the current interest rate (default 7%). Assume all accounts have the same interest rate.
 A private Date data field named dateCreated that stores the date when the account was created.
 A no-arg constructor that creates a default account.
 A constructor that creates an account with the specified id and initial balance.
 The accessor and mutator methods for id, balance, and annualInterestRate.
 The accessor method for dateCreated.
 A method named getMonthlyInterestRate() that returns the monthly interest rate.
 A method named getMonthlyInterest() that returns the monthly interest.
 A method named withdraw that withdraws a specified amount from the account.
 A method named deposit that deposits a specified amount to the account.* 
 
 */

 /*
 import java.util.Date;

public class Account {
    private int id;
    private double balance;
    private double annualInterestRate;
    private Date dateCreated;

    public Account() {
        id = 0;
        balance = 500;
        annualInterestRate = 0.07;
        dateCreated = new Date();
    }

    public Account(int id, double balance) {
        this.id = id;
        this.balance = balance;
        annualInterestRate = 0.07;
        dateCreated = new Date();
    }

    public int getId() 
    {
        return id;
    }

    public void setId(int id)
     {
        this.id = id;
    }

    public double getBalance() 
    {
        return balance;
    }

    public void setBalance(double balance)
     {
        this.balance = balance;
    }

    public double getAnnualInterestRate()
     {
        return annualInterestRate;
    }

    public void setAnnualInterestRate(double annualInterestRate) 
    {
        this.annualInterestRate = annualInterestRate;
    }

    public Date getDateCreated() 
    {
        return dateCreated;
    }

    public double getMonthlyInterestRate()
     {
        return annualInterestRate / 12;
    }

    public double getMonthly_INTERST()
     {
        return balance * getMonthlyInterestRate();
    }

    public void withdraw(double amount) 
    {
        balance -= amount;
    }

    public void deposit(double amount) {
        balance += amount;
    }
    
    public static void main(String[] args) {
        Account account = new Account(22, 50000);
        account.deposit(6000);
        account.withdraw(500);
        System.out.println("BALANCE :  " + account.getBalance());
        System.out.println("MONTHLY INTEREST :  " + account.getMonthly_INTERST());
        System.out.println("DATE CREATED : " + account.getDateCreated());
    }
}
*/


import java.util.Scanner;

public class Account
 {
    private float productNo;
    private String productName;
    private String activationKey;
    private float priceofProduct;

    public Account(float productNo, String productName, String activationKey, float priceofProduct) {
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
        Account[] key = new Account[5];
        Scanner sc = new Scanner(System.in);
        for (int i = 0; i < key.length; i++) {
            System.out.println("ENTER DETAILS FOR PRODUCT No." + (i + 1) + ":");
            System.out.print("PRODUCT NO: ");
            float productNo = sc.nextFloat();
            sc.nextLine();
            System.out.print("PRODUCT NAME: ");
            String productName = sc.nextLine();
            System.out.print("PRODUCT ACTIVATION KEY: ");
            String activationKey = sc.nextLine();
            System.out.print("PRODUCT'S PRICE: ");
            float priceofProduct = sc.nextFloat();
            sc.nextLine();

            key[i] = new Account(productNo, productName, activationKey, priceofProduct);
        }
        System.out.print("ENTER PRODUCT NAME TO SEARCH: ");
        String searchProductName = sc.nextLine();
        System.out.print("ENTER PRODUCT NUMBER TO SEARCH: ");
        float searchProductNo = sc.nextFloat();
        for (Account product : key) 
        
        {
            if (product.getProductName().equalsIgnoreCase(searchProductName) && product.getProductNo() == searchProductNo) 
            {
                product.display();
                break;
            }
        }
        sc.close();
    }
}



