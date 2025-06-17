def get_intervals(
    times: list[int], lesson_start: int, lesson_end: int
) -> list[int]:
    """
    Возвращает интервалы, ограниченные рамками урока.

    Аргументы:
        times (list[int]): Временные метки входа и выхода.
        lesson_start (int): Начало урока.
        lesson_end (int): Конец урока.

    Возвращает:
        list[int]: Список кортежей (вход, выход) внутри урока.
    """
    intervals = []
    for index in range(0, len(times), 2):
        start = max(times[index], lesson_start)
        end = min(times[index + 1], lesson_end)
        if start < end:
            intervals.append((start, end))
    return intervals


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика
    и преподавателя на уроке.

    Аргументы:
        intervals (dict[str, list[int]]): Словарь с интервалами урока, ученика
        и преподавателя.

    Возвращает:
        int: Время одновременного присутствия в секундах.
    """
    lesson_start, lesson_end = intervals['lesson']
    pupil_times = intervals['pupil']
    tutor_times = intervals['tutor']

    pupil_intervals = get_intervals(pupil_times, lesson_start, lesson_end)
    tutor_intervals = get_intervals(tutor_times, lesson_start, lesson_end)

    overlap_intervals = []
    pupil_index = 0
    tutor_index = 0

    while (pupil_index < len(pupil_intervals)
           and tutor_index < len(tutor_intervals)):
        pupil_start, pupil_end = pupil_intervals[pupil_index]
        tutor_start, tutor_end = tutor_intervals[tutor_index]
        overlap_start = max(pupil_start, tutor_start)
        overlap_end = min(pupil_end, tutor_end)

        if overlap_start < overlap_end:
            overlap_intervals.append((overlap_start, overlap_end))
        if pupil_end < tutor_end:
            pupil_index += 1
        else:
            tutor_index += 1

    if not overlap_intervals:
        return 0

    overlap_intervals.sort()
    merged_intervals = [overlap_intervals[0]]

    for start, end in overlap_intervals[1:]:
        last_start, last_end = merged_intervals[-1]
        if start <= last_end:
            merged_intervals[-1] = (last_start, max(last_end, end))
        else:
            merged_intervals.append((start, end))

    total_overlap_time = 0
    for start, end in merged_intervals:
        total_overlap_time += end - start

    return total_overlap_time
