def func(a, b, x2, tables, table_ind):
    rt = tables[table_ind].temperature*8.314462618    # температура на газовую постоянную
    x1 = 1 - x2
    return rt * x1 * x2*(x1 * a + x2 * b)
def sum_of_deviations(a, b, tables, table_ind, l_points):
    sum = 0
    for i in range(0, len(l_points)):
        x2 = l_points[i][0]
        ge = l_points[i][1]
        sum += (func(a, b, x2, tables, table_ind) - ge) ** 2
    return sum / len(l_points)
def gauss_step(tables, table_ind):
    l_points = []
    for point in tables[table_ind].points.all():
        l_points.append((point.x_value, point.y_value))
    a, b = 1, 1
    eps = 0.0000001
    flag = True
    count = 0
    f_stepa, f_stepb, b_stepa, b_stepb = True, True, True, True
    count_iter_a, count_iter_b = 0, 0
    const_learning = 1.01
    da, db = 0.001, 0.001
    iter_max = 10
    while flag:
        pa, pb = a, b
        if count_iter_a >= iter_max:
            da *= const_learning
        else:
            da = 0.0001
        if count_iter_b >= iter_max:
            db *= const_learning
        else:
            db = 0.0001
        if sum_of_deviations(a + da, b, tables, table_ind, l_points) < sum_of_deviations(a, b, tables, table_ind, l_points):
            a += da
            if b_stepa:
                f_stepa, b_stepa = True, False
                count_iter_a = 0
            count_iter_a += 1
        elif sum_of_deviations(a - da, b, tables, table_ind, l_points) < sum_of_deviations(a, b, tables, table_ind, l_points):
            a -= da
            if f_stepa:
                f_stepa, b_stepa = False, True
                count_iter_a = 0
            count_iter_a += 1
        if sum_of_deviations(a, b + db, tables, table_ind, l_points) < sum_of_deviations(a, b, tables, table_ind, l_points):
            b += db
            if b_stepb:
                f_stepb, b_stepb = True, False
                count_iter_b = 0
            count_iter_b += 1
        elif sum_of_deviations(a, b - db, tables, table_ind, l_points) < sum_of_deviations(a, b, tables, table_ind, l_points):
            b -= db
            if f_stepb:
                f_stepb, b_stepb = False, True
                count_iter_b = 0
            count_iter_b += 1
        count += 1
        flag = abs(sum_of_deviations(a, b, tables, table_ind, l_points) - sum_of_deviations(pa, pb, tables, table_ind, l_points)) > eps
        print(a, b, "gauss_step", table_ind)
    return a, b