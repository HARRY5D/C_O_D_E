public class dsa4_1 {
        Node head;
        Node tail;
    
        class Node {
            int data;
            Node prev;
            Node next;
    
            Node(int d) {
                data = d;
                prev = null;
                next = null;
            }
        }
    
        public void insertAtFront(int data) {
            Node newNode = new Node(data);
            if (head == null) {
                head = newNode;
                tail = newNode;
            } else {
                newNode.next = head;
                head.prev = newNode;
                head = newNode;
            }
            DISPLAYCONTENT();
        }
    
        public void deleteAtLast() {
            if (head == null) {
                System.out.println("LIST IS EMPTY");
            } else if (head == tail) {
                head = null;
                tail = null;
            } else {
                Node temp = head;
                while (temp.next != tail) {
                    temp = temp.next;
                }
                temp.next = null;
                tail = temp;
            }
            DISPLAYCONTENT();
        }
    
        public void deleteAllNodes() {
            head = null;
            tail = null;
            DISPLAYCONTENT();
        }
    
        public void DISPLAYCONTENT() {
            Node temp = head;
            while (temp != null) {
                System.out.print(temp.data + " ");
                temp = temp.next;
            }
            System.out.println();
        }
    
        public static void main(String[] args) {
            dsa4_1 dll = new dsa4_1();
            dll.insertAtFront(5);
            dll.insertAtFront(10);
            dll.insertAtFront(15);
            dll.insertAtFront(20);
            dll.deleteAtLast();
            dll.deleteAllNodes();
        }
    }
