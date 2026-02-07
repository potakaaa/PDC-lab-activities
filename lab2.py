import math
import threading
from multiprocessing import Process, Queue
import os

print_lock = threading.Lock()

def worker_threading_gwa(thread_id, grades, results):
    partial_sum = sum(grades)
    partial_count = len(grades)

    with print_lock:
        print(f"\n[Thread {thread_id}] Starting computation...")
        
        if not grades:
            print(f"[Thread {thread_id}] No grades provided.")
            return
        
        gwa = sum(grades) / len(grades)
        print(f"[Thread {thread_id}] Grades: {grades}")
        print(f"[Thread {thread_id}] Partial GWA: {gwa:.2f}")
        print(f"[Thread {thread_id}] Finished.\n")

    results.append((partial_sum, partial_count))

def run_threading_gwa(grades_list):
    if not grades_list:
        print("No grades to compute")
        return

    try:
        val = input("Enter number of threads: ")
        num_threads = int(val)
        if num_threads <= 0:
            print("Number of threads must be greater than 0.")
            return
    except ValueError:
        print("Invalid input.")
        return

    threads = []
    results = [] 
    chunk_size = math.ceil(len(grades_list) / num_threads)
        
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size
        chunk = grades_list[start:end]

        if not chunk:
            break

        t = threading.Thread(
            target=worker_threading_gwa,
            args=(i + 1, chunk, results)
        )
        threads.append(t)
        t.start()
        print(f"[Main] Thread {i + 1} started.")

    for t in threads:
        t.join()

    if not results:
        print("[Main] No results calculated.")
        return

    total_sum = sum(result[0] for result in results)
    total_count = sum(result[1] for result in results)
    
    if total_count > 0:
        final_gwa = total_sum / total_count
        print(f"\n[Main] Final GWA (Multithreading): {final_gwa:.2f}")
    else:
        print("\n[Main] Total count is zero.")
        
    print("[Main] All threads finished.")

def worker_multiprocessing_gwa(grades_chunk, queue, proc_id):
    print(f"[Process-{proc_id} | PID {os.getpid()}] STARTING with grades: {grades_chunk}")
    if not grades_chunk:
        queue.put((0, 0))
        return

    partial = sum(grades_chunk) / len(grades_chunk)
    print(f"[Process-{proc_id} | PID {os.getpid()}] Partial GWA: {partial:.2f}")
    print(f"[Process-{proc_id} | PID {os.getpid()}] ENDING")
    queue.put((sum(grades_chunk), len(grades_chunk)))

def run_multiprocessing_gwa(grades):
    if not grades:
        print("No grades to compute.")
        return

    while True:
        try:
            val = input(f"Enter number of processes (1-{len(grades)}): ")
            num_processes = int(val)
            if 1 <= num_processes <= len(grades):
                break
            else:
                print(f"Please enter a number between 1 and {len(grades)}")
        except ValueError:
            print("Invalid input. Enter an integer.")

    chunk_size = max(1, len(grades) // num_processes)
    grade_chunks = [grades[i:i+chunk_size] for i in range(0, len(grades), chunk_size)]

    q = Queue()
    processes = []

    for i, chunk in enumerate(grade_chunks, start=1):
        p = Process(target=worker_multiprocessing_gwa, args=(chunk, q, i))
        processes.append(p)
        p.start()

    total_sum = 0
    total_count = 0
    
    for _ in grade_chunks:
        partial_sum, count = q.get()
        total_sum += partial_sum
        total_count += count

    for p in processes:
        p.join()

    if total_count > 0:
        global_gwa = total_sum / total_count
        print(f"\n[Main] Global GWA (Multiprocessing): {global_gwa:.2f}")
    else:
        print("[Main] Total count is 0.")

def main():
    grades_list = []
    print("--- Unified Grade Calculator ---")

    while True:
        print("\n1. Add Grade")
        print("2. Compute GWA")
        print("3. Exit")
        
        try:
            choice = input("\nEnter option: ") 

            if choice == '1':
                try:
                    val = input("Enter grade: ")
                    grade = float(val)
                    grades_list.append(grade)
                    print(f"Grade {grade} added successfully.")
                except ValueError:
                    print("Invalid grade. Must be a number.")

            elif choice == '2':
                if not grades_list:
                    print("No grades to compute.")
                    continue
                
                print("\nSelect Computation Method:")
                print("1. Multithreading")
                print("2. Multiprocessing")
                print("3. Cancel")
                
                method = input("Enter method: ")
                
                if method == '1':
                    run_threading_gwa(grades_list)
                    break
                elif method == '2':
                    run_multiprocessing_gwa(grades_list)
                    break
                elif method == '3':
                    print("Cancelled computation.")
                else:
                    print("Invalid method selected.")
            
            elif choice == '3':
                print("Exiting program...")
                break
             
            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
