from aiogram.dispatcher.filters.state import StatesGroup, State


class UserInfoData(StatesGroup):
    state_name = State()
    state_age = State()
    state_kurs = State()
    state_phone_number = State()    
    state_check = State()
    
    



class KursInfoData(StatesGroup):
    nomi = State()
    vaqti = State()
    davomiylik = State()
    narxi= State()
    discr = State()
    photo = State()
    tasdiqlash = State()
       


class AdminData(StatesGroup):
    kurs_name = State()
    kurs_name_ust = State()
    kurs_new_inf = State()
    


class AdminRecData(StatesGroup):
    rekl_rasm = State()
    rekl_text = State()
    rekl_knopka = State()
    rekl_tasdiq = State()
    rekl_url = State()
    rekl_url_text = State()
    rekl_url_manz = State()