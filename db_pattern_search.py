def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    # создаем матрицу для хранения расстояний
    distances = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        distances[i][0] = i
    for j in range(n + 1):
        distances[0][j] = j

    # считаем расстояния
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                distances[i][j] = distances[i - 1][j - 1]
            else:
                substitute_cost = distances[i - 1][j - 1] + 1
                insert_cost = distances[i][j - 1] + 1
                delete_cost = distances[i - 1][j] + 1
                distances[i][j] = min(substitute_cost, insert_cost, delete_cost)

    return distances[m][n]


def find_username(first_name, last_name, database):
    min_distance = float('inf')
    matching_chat_id = None

    for entry in database:
        _, db_first_name, db_last_name, _, chat_id = entry
        first_name_distance = levenshtein_distance(first_name, db_first_name)
        last_name_distance = levenshtein_distance(last_name, db_last_name)

        avg_distance = (first_name_distance + last_name_distance) / 2

        if avg_distance < min_distance:
            min_distance = avg_distance
            matching_chat_id = chat_id

    return matching_chat_id
