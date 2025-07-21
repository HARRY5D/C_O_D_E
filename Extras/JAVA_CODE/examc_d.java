//package task_management;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.*;

enum Priority { HIGH, MEDIUM, LOW;}

class Task 
{
    private static int nextId = 1;
    private int id;
    private String description;
    private LocalDate dueDate;
    private Priority priority;
    private boolean completed;

    public Task(String description, LocalDate dueDate, Priority priority) {
        this.id = nextId++;
        this.description = description;
        this.dueDate = dueDate;
        this.priority = priority;
        this.completed = false;
    }

    // Getters and setters
    public int getId() { return id; }
    public String getDescription() { return description; }
    public LocalDate getDueDate() { return dueDate; }
    public Priority getPriority() { return priority; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) 
    { this.completed = completed; }
}

class TaskManager 
{
    private List<Task> tasks = new ArrayList<>();
        
    private Scanner scanner = new Scanner(System.in);
    private DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

   

    public void addTask() {
        try {
            System.out.print("Enter task description: ");
            String description = scanner.nextLine().trim();
            if (description.isEmpty()) {
                throw new IllegalArgumentException("Task description cannot be empty");
            }

            System.out.print("Enter due date (yyyy-MM-dd): ");
            LocalDate dueDate = LocalDate.parse(scanner.nextLine(), dateFormatter);
            if (dueDate.isBefore(LocalDate.now())) {
                throw new IllegalArgumentException("Due date must be in the future");
            }

            System.out.print("Enter priority (HIGH/MEDIUM/LOW): ");
            Priority priority = Priority.valueOf(scanner.nextLine().toUpperCase());

            Task task = new Task(description, dueDate, priority);
            tasks.add(task);
            System.out.println("Task added successfully!");
        } catch (DateTimeParseException e) {
            System.out.println("Invalid date format. Please use yyyy-MM-dd");
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public void markTaskComplete() {
        System.out.print("Enter task ID to mark as complete: ");
        try {
            int taskId = Integer.parseInt(scanner.nextLine());
            Optional<Task> task = tasks.stream()
                .filter(t -> t.getId() == taskId)
                .findFirst();
            
            if (task.isPresent()) {
                task.get().setCompleted(true);
                System.out.println("Task marked as complete!");
            } else {
                System.out.println("Task not found.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid task ID");
        }
    }

    public void viewAllTasks() {
        if (tasks.isEmpty()) {
            System.out.println("No tasks found.");
            return;
        }
        
        System.out.println("\nAll Tasks:");
        tasks.forEach(this::printTask);
    }

    public void viewPendingTasks() {
        List<Task> pendingTasks = tasks.stream()
            .filter(task -> !task.isCompleted())
            .toList();

        if (pendingTasks.isEmpty()) {
            System.out.println("No pending tasks.");
            return;
        }

        System.out.println("\nPending Tasks:");
        pendingTasks.forEach(this::printTask);
    }

    private void printTask(Task task) {
        System.out.printf("ID: %d | Description: %s | Due Date: %s | Priority: %s | Status: %s%n",
            task.getId(),
            task.getDescription(),
            task.getDueDate().format(dateFormatter),
            task.getPriority(),
            task.isCompleted() ? "Completed" : "Pending"
        );
    }

    public void searchTasks() {
        System.out.print("Enter search term (description or date yyyy-MM-dd): ");
        String searchTerm = scanner.nextLine().trim();
        
        List<Task> matchingTasks = new ArrayList<>();
        
        try {
            LocalDate searchDate = LocalDate.parse(searchTerm, dateFormatter);
            matchingTasks = tasks.stream()
                .filter(task -> task.getDueDate().equals(searchDate))
                .toList();
        } catch (DateTimeParseException e) {
            matchingTasks = tasks.stream()
                .filter(task -> task.getDescription().toLowerCase().contains(searchTerm.toLowerCase()))
                .toList();
        }

        if (matchingTasks.isEmpty()) {
            System.out.println("No matching tasks found.");
            return;
        }

        System.out.println("\nMatching Tasks:");
        matchingTasks.forEach(this::printTask);
    }

    public void start() {
        while (true) {
            System.out.println("\n=== Task Management System ===");
            System.out.println("1. Add Task");
            System.out.println("2. Mark Task as Complete");
            System.out.println("3. View All Tasks");
            System.out.println("4. View Pending Tasks");
            System.out.println("5. Search Tasks");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");

            try {
                int choice = Integer.parseInt(scanner.nextLine());
                switch (choice) {
                    case 1 -> addTask();
                    case 2 -> markTaskComplete();
                    case 3 -> viewAllTasks();
                    case 4 -> viewPendingTasks();
                    case 5 -> searchTasks();
                    case 6 -> {
                        System.out.println("Goodbye!");
                        return;
                    }
                    default -> System.out.println("Invalid choice. Please try again.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a number.");
            }
        }
    }
}

public class examc_d
 {
    public static void main(String[] args) {
        TaskManager manager = new TaskManager();
        manager.start();
    }
}
