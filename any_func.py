

def checking_occurrence(list_checking, *args):
    for i in args:
        if i not in list_checking:
            return False

    return True