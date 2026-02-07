import math
import threading
import time

print_lock = threading.Lock()
results = []

def compute_gwa(thread_id, grades):
    """
    Function to compute GWA in a separate thread.
    """

    partial_sum = sum(grades)
    partial_count = len(grades)

    with print_lock:
        print(f"\n[Thread {thread_id}] Starting computation...")
        
        if not grades:
            print(f"[Thread {thread_id}] No grades provided.")
            return
        
        gwa = sum(grades) / len(grades)
        print(f"[Thread {thread_id}] Grades: {grades}\n")
        print(f"[Thread {thread_id}] Partial GWA: {gwa:.2f}")
        print(f"[Thread {thread_id}] Finished.\n")

    results.append((partial_sum, partial_count))

grades_list = []

print("--- Multithreaded Grade Calculator ---")


while True:
    print("\n1. Add Grade")
    print("2. Compute GWA")
    print("3. Exit")
    
    try:
        option = int(input("\nEnter option: "))

        if option == 1:
            grade = int(input("\nEnter grade: "))
            grades_list.append(grade)
            print(f"Grade {grade} added successfully.")

        elif option == 2:
            if len(grades_list) == 0:
                print("No grades to compute")
                continue

            num_threads = int(input("Enter number of threads: "))
            if num_threads <= 0:
                print("Number of threads must be greater than 0.")
                continue

            threads = []
            chunk_size = math.ceil(len(grades_list) / num_threads)
                
            for i in range(num_threads):
                start = i * chunk_size
                end = start + chunk_size
                chunk = grades_list[start:end]

                if not chunk:
                    break

                t = threading.Thread(
                    target=compute_gwa,
                    args=(i + 1, chunk)
                )
                threads.append(t)
                t.start()

                print(f"[Main] Thread {i + 1} started.")

            for t in threads:
                t.join()

            total_sum = sum(result[0] for result in results)
            total_count = sum(result[1] for result in results)
            final_gwa = total_sum / total_count

            print(f"\n[Main] Final GWA: {final_gwa:.2f}")

            print("\n[Main] All threads finished.")
            break
            
        elif option == 3:
            print("Exiting program...")
            break
         
        else:
            print("Invalid option. Please try again.")
            continue

    except:
        print("Invalid input. Please enter a valid one.")
        continue


