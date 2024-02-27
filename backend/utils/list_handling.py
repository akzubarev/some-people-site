from typing import Sequence


def batched(lst: Sequence, batch_size: int):
    if batch_size is None:
        return lst
    elif batch_size == 1:
        return [[obj] for obj in lst]
    else:
        return [lst[i:i + batch_size] for i in range(0, len(lst), batch_size)]
