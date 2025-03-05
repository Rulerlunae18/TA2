import os


def merge_and_count(arr, temp_arr, left, mid, right):
    i = left
    j = mid + 1
    k = left
    inv_count = 0

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            temp_arr[k] = arr[j]
            inv_count += (mid - i + 1)  # Підрахунок кількості інверсій
            j += 1
        k += 1

    while i <= mid:
        temp_arr[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp_arr[k] = arr[j]
        j += 1
        k += 1

    for i in range(left, right + 1):
        arr[i] = temp_arr[i]

    return inv_count


def merge_sort_and_count(arr, temp_arr, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2
        inv_count += merge_sort_and_count(arr, temp_arr, left, mid)
        inv_count += merge_sort_and_count(arr, temp_arr, mid + 1, right)
        inv_count += merge_and_count(arr, temp_arr, left, mid, right)
    return inv_count


def count_inversions(arr):
    if not arr:  # Перевірка масива
        return 0, []

    temp_arr = arr.copy()
    inv_count = merge_sort_and_count(arr, temp_arr, 0, len(arr) - 1)
    return inv_count, arr  # Повертаємо кількість інверсій та відсортований масив


def main():
    file_path = r'example/input_2_1000.txt'  # Файл із даними
    output_file = r'example/output.txt'  # Файл для збереження результатів

    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не існує.")
        return
    if os.path.getsize(file_path) == 0:
        print("Файл порожній")
        return

    with open(file_path, 'r') as file:
        arr = file.read().splitlines()

    first_str = arr[0]
    users = first_str.split(' ')

    try:
        num_users = int(users[0])
        main_user = int(users[1])  # Основний користувач X
    except ValueError:
        print("Елемент має бути числом")
        return

    array_matrix = []
    for index_user in range(1, num_users + 1):
        try:
            num_arr = list(map(int, arr[index_user].split()))
        except ValueError:
            print("Елемент має бути числом")
            return

        user = num_arr[0]
        arr_el_of_user = num_arr[1:]
        for elem in arr_el_of_user:
            array_matrix.append([user, elem])

    similarity_list = []
    main_likes = [num for usr, num in array_matrix if usr == main_user]

    for user_id in range(1, num_users + 1):
        if user_id == main_user:
            continue
        likes = [num for usr, num in array_matrix if usr == user_id]
        if likes:
            inversions, _ = count_inversions(likes)
            similarity_list.append((user_id, inversions))

    similarity_list.sort(key=lambda x: x[1])  # Сортуємо за значенням c

    with open(output_file, 'w') as out_file:
        out_file.write(f"{main_user}\n")
        for user, inv_count in similarity_list:
            out_file.write(f"{user} {inv_count}\n")

    print(f"Результати записано у файл: {output_file}")


if __name__ == "__main__":
    main()
