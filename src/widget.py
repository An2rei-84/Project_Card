import masks

def mask_account_card(args: str) -> str:
    data_account = str(args)
    if "Счет" in data_account:
        return f"Счет {masks.get_mask_account(args)}"
    else:
        data_card = data_account.replace(data_account[-16:],"")
        return f"{data_card[0:]}{masks.mask_card_number(args[-16:])}"

print(mask_account_card('Visa Platinum 7000 7922 8960 6361'))



def get_data(arg: str) -> str:
    data_ = str(arg)
    return f"{data_[8:10]}.{data_[5:7]}.{data_[:4]}"




