#include <stdio.h>

int main() {
    float cgpa;
    int income, sportsQuota;

    printf("Enter CGPA: ");
    scanf("%f", &cgpa);

    printf("Enter Income: ");
    scanf("%d", &income);

    printf("Sports Quota (1 = Yes, 0 = No): ");
    scanf("%d", &sportsQuota);

    if (cgpa >= 8.5) {
        if (income < 400000) {
            printf("Scholarship Approved\n");
        } else {
            printf("Forwarded for Review\n");
        }
    } 
    else if (cgpa >= 7.0 && sportsQuota == 1) {
        printf("Sports Scholarship Approved\n");
    } 
    else {
        printf("Application Rejected\n");
    }

    return 0;
}