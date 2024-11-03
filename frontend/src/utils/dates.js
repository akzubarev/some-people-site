const months_dict = {
    0: 'янв',
    1: 'фев',
    2: 'мар',
    3: 'апр',
    4: 'мая',
    5: 'июн',
    6: 'июл',
    7: 'авг',
    8: 'сен',
    9: 'окт',
    10: 'ноя',
    11: 'дек',
}
export const formatDateRange = (start, end) => {
    if (!start || !end)
        return ''
    const start_date = start.getDate()
    const start_month = start.getMonth()
    const end_date = end.getDate()
    const end_month = end.getMonth()
    if (start_month == end_month)
        return `${start_date}-${end_date} ${months_dict[start_month]}`
    return `${start_date} ${months_dict[start_month]} - ${end_date} ${months_dict[end_month]}`
}