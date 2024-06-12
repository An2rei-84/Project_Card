import masks


def mask_account_card():
    pass



def get_data(arg: str) -> str:
    data_ = str(arg)
    return f"{data_[8:10]}.{data_[5:7]}.{data_[:4]}"


print(get_data('2018-07-11T02:26:18.671407'))
