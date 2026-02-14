"""
Philippine payroll deduction calculator using parallel computation.

Computes SSS, PhilHealth, Pag-IBIG, and income tax withholdings for monthly
salaries. Uses ThreadPoolExecutor for concurrent calculation of each
deduction type.
"""
import math
from concurrent.futures import ThreadPoolExecutor

# Sample employee data: (name, monthly_salary)
employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]

# Placeholder for computed salary data
salaries = []


def compute_sss(salary):
    """Compute SSS contribution (4.5% of salary, rounded up)."""
    return math.ceil(salary * 0.045)


def compute_philhealth(salary):
    """Compute PhilHealth contribution (2.5% of salary, rounded up)."""
    return math.ceil(salary * 0.025)


def compute_pagibig(salary):
    """
    Compute Pag-IBIG contribution.

    Rate is 10% if salary <= 1500, otherwise 20%. Rounded up.
    """
    return math.ceil(salary * 0.1 if salary <= 1500 else salary * 0.2)


def compute_tax(salary):
    """
    Compute monthly income tax withholding based on TRAIN law brackets.

    Converts monthly salary to annual for bracket lookup, then returns
    the monthly equivalent of the annual tax.
    """
    annual = salary * 12
    if annual <= 250_000:
        tax = 0
    elif annual <= 400_000:
        tax = (annual - 250_000) * 0.15
    elif annual <= 800_000:
        tax = 22_500 + (annual - 400_000) * 0.20
    elif annual <= 2_000_000:
        tax = 102_500 + (annual - 800_000) * 0.25
    elif annual <= 8_000_000:
        tax = 402_500 + (annual - 2_000_000) * 0.30
    else:
        tax = 2_202_500 + (annual - 8_000_000) * 0.35
    return math.ceil(tax / 12)


def parallel_compute(salary):
    """
    Compute all deductions in parallel using a thread pool.

    Returns a dict with keys: salary, sss, philhealth, pagibig, tax.
    """
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_sss = executor.submit(compute_sss, salary)
        future_philhealth = executor.submit(compute_philhealth, salary)
        future_pagibig = executor.submit(compute_pagibig, salary)
        future_tax = executor.submit(compute_tax, salary)

        return {
            "salary": salary,
            "sss": future_sss.result(),
            "philhealth": future_philhealth.result(),
            "pagibig": future_pagibig.result(),
            "tax": future_tax.result(),
        }


def print_deductions(deductions):
    """
    Print a receipt-style payslip showing gross salary, deductions, and net pay.

    Expects a dict from parallel_compute with salary, sss, philhealth,
    pagibig, and tax keys.
    """
    salary = deductions["salary"]
    sss = deductions["sss"]
    philhealth = deductions["philhealth"]
    pagibig = deductions["pagibig"]
    tax = deductions["tax"]
    total_deductions = sss + philhealth + pagibig + tax
    net_pay = salary - total_deductions

    width = 40
    print("=" * width)
    print("       PAYSLIP - DEDUCTION SUMMARY".center(width))
    print("=" * width)
    print(f"{'Description':<20} {'Amount':>15}")
    print("-" * width)
    print(f"{'Gross Salary':<20} {salary:>15,.2f}")
    print(f"{'SSS':<20} {sss:>15,.2f}")
    print(f"{'PhilHealth':<20} {philhealth:>15,.2f}")
    print(f"{'Pag-IBIG':<20} {pagibig:>15,.2f}")
    print(f"{'Income Tax':<20} {tax:>15,.2f}")
    print("-" * width)
    print(f"{'Total Deductions':<20} {total_deductions:>15,.2f}")
    print(f"{'NET PAY':<20} {net_pay:>15,.2f}")
    print("=" * width)


# Demo: compute and display deductions for a sample salary
salary = 1000000
print_deductions(parallel_compute(salary))