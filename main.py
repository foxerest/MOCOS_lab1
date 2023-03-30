from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


n = 5
interval_beginning = - np.pi
interval_end = np.pi
interval = interval_end - interval_beginning
precision_N = 50
file_name = "./result.txt"


def func_f(x):
    return n * np.sin(np.pi * n * x)


def integral_function_a_k(x, k):
    return (2 / interval) * func_f(x) * np.cos((2 * np.pi * k * x) / interval)


def integral_function_b_k(x, k):
    return (2 / interval) * func_f(x) * np.sin((2 * np.pi * k * x) / interval)


def calculate_fourier_k_harmonic(x, k):
    return find_coefficient_a_k(k) * np.cos((2 * np.pi * k * x) / interval) + \
           find_coefficient_b_k(k) * np.sin((2 * np.pi * k * x) / interval)


def calculate_approximate_value(x, number):
    return find_coefficient_a_k(0) / 2 + sum(calculate_fourier_k_harmonic(x, k) for k in range(1, number + 1))


def find_coefficient_a_k(k):
    a_k = integrate.quad(integral_function_a_k, interval_beginning, interval_end, args=k)
    return a_k[0]


def find_coefficient_b_k(k):
    b_k = integrate.quad(integral_function_b_k, interval_beginning, interval_end, args=k)
    return b_k[0]


def calculate_error(x):
    try:
        return (calculate_approximate_value(x, precision_N) - func_f(x)) / func_f(x)
    except RuntimeWarning:
        return 0


def output_and_write_massage(output_str, file_object):
    print(output_str)
    file_object.write(output_str + "\n")


def show_fourier_coefficients(file_object):
    th = ['k', 'a_k', 'b_k']
    td = []
    output_and_write_massage("\nКоефіцієнти тригонометричного ряду Фур'є", file_object)

    for k in range(0, precision_N + 1):
        td.append(k)
        if k == 0:
            td.append((round(find_coefficient_a_k(k), 6)))
            td.append("None")
            continue
        td.append((str(round(find_coefficient_a_k(k), 6))))
        td.append((str(round(find_coefficient_b_k(k), 6))))

    columns = len(th)
    table = PrettyTable(th)

    while td:
        table.add_row(td[:columns])
        file_object.write('a_{0:<3} = {1:<12} b_{0:<2} = {2:<12}'.format(*td[:columns]) + "\n")
        td = td[columns:]

    print(table)


def show_graphs():
    # Перший графік (Графік функції f та наближення функції f рядом Фур'є)
    fig1, ax1 = plt.subplots(1, 1, figsize=(10, 10))
    ax1.set_title("Графік функції f та наближення функції f рядом Фур'є", fontsize=16)
    plt.grid(True)
    x_1 = np.linspace(interval_beginning, interval_end, num=1000)
    plt.plot(x_1, func_f(x_1), label="Функція f", linewidth=3)
    plt.plot(x_1, calculate_approximate_value(x_1, precision_N), label="Наближення N = " + str(30), color="red")
    plt.xlim([interval_beginning, interval_end])
    plt.legend(borderaxespad=0.2, loc="best")
    plt.show()

    # Другий графік (Функція a(k) в частотній області)
    fig2, ax2 = plt.subplots(figsize=(10, 10))
    ax2.set_title('Функція a(k) в частотній області', fontsize=16)
    plt.grid(True)
    for i in range(0, precision_N + 1):
        a_value = find_coefficient_a_k(i)
        plt.plot(i, a_value, 'ro-')
        plt.plot([i, i], [0, a_value], 'r-')
    plt.show()

    # Третій графік (Функція b(k) в частотній області)
    fig3, ax3 = plt.subplots(figsize=(10, 10))
    ax3.set_title('Функція b(k) в частотній області', fontsize=16)
    plt.grid(True)
    for i in range(1, precision_N + 1):
        b_value = find_coefficient_b_k(i)
        plt.plot(i, b_value, 'bo-')
        plt.plot([i, i], [0, b_value], 'b-')
    plt.show()

    # Четвертий графік (Графік функції f та поступове наближення функції f рядом Фур'є)
    fig4, ax4 = plt.subplots(1, 1, figsize=(10, 10))
    ax4.set_title("Графік функції f та поступове наближення функції f рядом Фур'є", fontsize=16)
    plt.grid(True)
    x_2 = np.linspace(interval_beginning, interval_end, num=1000)
    plt.xlim([interval_beginning, interval_end])
    plt.plot(x_2, func_f(x_2), label="Функція f")
    for i in range(1, precision_N + 1, 4):
        plt.plot(x_2, calculate_approximate_value(x_2, i), label="Наближення N = " + str(i))
    plt.legend(borderaxespad=0.2, loc="best")
    plt.show()

    # П'ятий графік(рафік відносної похибки апроксимації)
    fig5, ax5 = plt.subplots(1, 1, figsize=(10, 10))
    ax5.set_title("Графік відносної похибки апроксимації", fontsize=16)
    plt.grid(True)
    x_3 = np.linspace(interval_beginning+0.01, interval_end-0.01, num=3500)
    plt.xlim([interval_beginning, interval_end])
    plt.plot(x_3, ((calculate_approximate_value(x_3, precision_N) - func_f(x_3)) / func_f(x_3))*100, label="Значення відносної похибки")
    plt.legend(borderaxespad=0.2, loc="best")
    plt.show()


def main_func():
    file_object = open(file_name, "w", encoding="utf-8")
    output_and_write_massage("Програма обчислить наближене за допомогою ряду Фур'є значення функції\nn * "
                             "sin(pi * n * x), де n = {}, на проміжку х є [{}; "
                             "{}]".format(n, interval_beginning, interval_end), file_object)
    show_graphs()
    show_fourier_coefficients(file_object)
    file_object.close()
    return 0


main_func()
