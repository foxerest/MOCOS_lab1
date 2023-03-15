from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


n = 13
interval_beginning = 0
interval_end = np.pi
interval = interval_end - interval_beginning
precision_N = 30
file_name = "./result.txt"


def func_f(x):
    return n * np.sin(np.pi * n * x)


def integral_function_a_k(x, k):
    return (2 / interval) * func_f(x) * np.cos((2 * np.pi * k * x) / interval)


def integral_function_b_k(x, k):
    return (2 / interval) * func_f(x) * np.sin((2 * np.pi * k * x) / interval)


def calculate_function_value(x):
    return func_f(x)


def calculate_fourier_k_harmonic(x, k):
    return find_coefficient_a_k(k) * np.cos((2 * np.pi * k * x) / interval) + \
           find_coefficient_b_k(k) * np.sin((2 * np.pi * k * x) / interval)


def calculate_approximate_value(x):
    suma = sum(calculate_fourier_k_harmonic(x, k) for k in range(1, precision_N + 1))
    return find_coefficient_a_k(0) / 2 + suma


def find_coefficient_a_k(k):
    a_k = integrate.quad(integral_function_a_k, interval_beginning, interval_end, args=k)
    return a_k[0]


def find_coefficient_b_k(k):
    b_k = integrate.quad(integral_function_b_k, interval_beginning, interval_end, args=k)
    return b_k[0]


def calculate_error(real_value, approximate_value):
    if round(real_value, 6) != 0:
        return "Відносна похибка: " + str(round(abs((real_value - approximate_value) * 100 / real_value), 6)) + " %"
    else:
        return "Відносну похибку не можливо порахувати оскільки y_real = " + str(round(real_value, 6)) + \
               "\nАбсолютна похибка : " + str(round(abs(real_value - approximate_value), 6))


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
    # Перший графік
    fig1, ax1 = plt.subplots(1, 1, figsize=(10, 10))
    ax1.set_title("Графік функції f та наближення функції f рядом Фур'є", fontsize=16)
    plt.grid(True)
    x_1 = np.linspace(0, np.pi, num=1000)
    plt.plot(x_1, calculate_function_value(x_1), label="Функція f")
    plt.plot(x_1, calculate_approximate_value(x_1), label=f"Наближення функції f рядом Фур'є")
    plt.legend(bbox_to_anchor=(0.4, -0.03), borderaxespad=0.2)
    plt.show()

    # Другий графік
    fig2, ax2 = plt.subplots(figsize=(10, 10))
    ax2.set_title('Функція a(k) в частотній області', fontsize=16)
    plt.grid(True)
    for i in range(0, precision_N + 1):
        a_value = find_coefficient_a_k(i)
        plt.plot(i, a_value, 'ro-')
        if i % 2 == 0:
            plt.text(i - 0.3, a_value + (0.3 if a_value > 0 else -0.5), "a_" + str(i))
        plt.plot([i, i], [0, a_value], 'r-')
    plt.show()

    # Третій графік
    fig3, ax3 = plt.subplots(figsize=(10, 10))
    ax3.set_title('Функція b(k) в частотній області', fontsize=16)
    plt.grid(True)
    for i in range(1, precision_N + 1):
        b_value = find_coefficient_b_k(i)
        plt.plot(i, b_value, 'bo-')
        if i % 2 != 0:
            plt.text(i - 0.3, b_value + (0.1 if b_value > 0 else -0.1), "b_" + str(i))
        plt.plot([i, i], [0, b_value], 'b-')
    plt.show()

    # Четвертий графік
    fig4, ax4 = plt.subplots(figsize=(10, 10))
    ax4.set_title("Графіки гармонік", fontsize=16)
    plt.grid(True)
    x_4 = np.linspace(0, np.pi, num=1000)
    # plt.plot(x_4, calculate_function_value(x_1), linewidth=3, color='crimson')
    for i in range(1, precision_N + 1):
        plt.plot(x_4, calculate_fourier_k_harmonic(x_4, i))
    plt.show()


def main_func():
    file_object = open(file_name, "w", encoding="utf-8")
    output_and_write_massage("Програма обчислить наближене за допомогою ряду Фур'є значення функції" +
                             "\nn * np.sin(np.pi * n * x), де n = " + str(n) + ", у точці х, яку введе користувач.",
                             file_object)
    try:
        input_x = float(input("Введіть значення х:"))
    except ValueError:
        print("Значення х повинне бути числовим!")
        return 0
    float(input_x)
    if not (interval_beginning <= input_x <= interval_end):
        print("Допустимі значення х: [" + str(round(interval_beginning, 6)) + "; "
              + str(round(interval_end, 6)) + "]")
        return 0
    output_and_write_massage("Значення х = " + str(input_x), file_object)
    y_real = calculate_function_value(input_x)
    y_fourier = calculate_approximate_value(input_x)
    output_and_write_massage("Обчислимо значення функції n * np.sin(np.pi * n * x) у точці: \nх = " + str(input_x),
                             file_object)
    output_and_write_massage("Аналітичне обчислення значення функції: \ny_real = " + str(round(y_real, 6)),
                             file_object)
    output_and_write_massage(
        "Наближене значення фунції, обчислене рядом Фур’є: \ny_fourier = " + str(round(y_fourier, 6)), file_object)
    output_and_write_massage(calculate_error(y_real, y_fourier), file_object)
    show_graphs()
    show_fourier_coefficients(file_object)
    file_object.close()
    return 0


main_func()
