import logging
from aiogram import Bot, Dispatcher, executor, types
from buttons import *
from  locations import *
from config import API_TOKEN, ADMIN
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from state import UserInfoData, KursInfoData, AdminData, AdminRecData
from baza import Database
from aiogram.dispatcher.filters import Text
storage = MemoryStorage()



bot =Bot(token=API_TOKEN)
dp=Dispatcher(bot, storage=storage)
db=Database()


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)
db.create_table()
db.create_table_kurs()
db.create_table_filial()

# ================================ start ===========================================================


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    telegram_id=message.from_user.id
    username = message.from_user.username
    user = db.select_user(telegram_id)
    if user is None:
        db.insert_user(telegram_id, username)
    await message.answer("Tanlang: ", reply_markup=menu)
    
    


@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    await message.answer("Xush kelibsiz, Admin: ", reply_markup=admin)
    



# ==================================   admin  ==============================================


@dp.message_handler(text="Kurs qo'shish")
async def kurs_q(message: types.Message):
    await message.answer("Yangi kurs nomini kiriting: ", reply_markup=types.ReplyKeyboardRemove())
    await KursInfoData.nomi.set()



@dp.message_handler(state=KursInfoData.nomi)
async def nom(message: types.Message, state: FSMContext):
    await state.update_data(nomi=message.text)
    await message.answer("Yangi kursning vaqtini kiriting: ")
    await KursInfoData.vaqti.set()
    
    
@dp.message_handler(state=KursInfoData.vaqti)
async def vaqt(message: types.Message, state: FSMContext):
    await state.update_data(vaqti=message.text)
    await message.answer("Yangi kurs davomiyligini kiriting: ")
    await KursInfoData.davomiylik.set()


@dp.message_handler(state=KursInfoData.davomiylik)
async def davom(message: types.Message, state: FSMContext):
    await state.update_data(davomiylik=message.text)
    await message.answer("Yangi kurs narxini kiriting: ")
    await KursInfoData.narxi.set()


@dp.message_handler(state=KursInfoData.narxi)
async def narx(message: types.Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await message.answer("Yangi kursda nimalar o'rgatiladi: ")
    await KursInfoData.discr.set()
    
    
@dp.message_handler(state=KursInfoData.discr)
async def discrip(message: types.Message, state: FSMContext):
    await state.update_data(discr=message.text)
    await message.answer("Yangi kurs uchun rasm yuboring: ")
    await KursInfoData.photo.set()
    



@dp.message_handler(content_types="photo", state=KursInfoData.photo)
async def raqam(message: types.Message, state: FSMContext):  
    foto = message.photo[-1].file_id
    await state.update_data(photo=foto)
    data = await state.get_data()
    nomi_= data.get("nomi")
    vaqti_= data.get("vaqti")
    davom = data.get("davomiylik")
    narxi_= data.get("narxi")
    disc_ = data.get("discr")
    photo_= data.get("photo")
    info = f"""
    {nomi_}
    
⏰ Dars vaqti: {vaqti_}

📅 Kurs davomiyligi: {davom}

💸 Kurs narxi oyiga {narxi_} so'm

Nimalarni o‘rgatamiz ?:

{disc_}

📌Kurs davomida shaxsiy portfoilo yaratasiz. 

🚀Darslarda 100% amaliy bilimlarga ega bo'lasiz.
    
    """

    await message.answer_photo(photo=photo_, caption=info, reply_markup=tasdiq_admin_kurs)
    await KursInfoData.tasdiqlash.set()
    



@dp.callback_query_handler(text="ha_adm", state=KursInfoData.tasdiqlash)
async def cheek(call:types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    nomi__= data.get("nomi")
    vaqti__= data.get("vaqti")
    davom_ = data.get("davomiyligi")
    narxi__= data.get("narxi")
    disc__ = data.get("discr")
    photo__= data.get("photo")
    db.insert_kurs(nomi__, vaqti__, davom_, narxi__, disc__, photo__)   
    await call.message.answer("Yangi kurs qo'shildi! ", reply_markup=admin)
    
    
    
    await state.finish()
    await state.reset_state()



@dp.callback_query_handler(text="yo'q_adm")
async def cheek(call:types.CallbackQuery):
    await call.message.answer("Tanlang ! ", reply_markup=kurs_tahlil)





@dp.message_handler(text="Kurslarni yangilash / o'chirirsh")
async def ozgar(message: types.Message):
    await message.answer("O'zgartirmoqchi bo'lgan kursingizni nomini kiriting", reply_markup=types.ReplyKeyboardRemove())
    
    await AdminData.kurs_name.set()


@dp.message_handler(state=AdminData.kurs_name)
async def k_nom(message: types.Message, state: FSMContext):
    await state.update_data(kurs_name=message.text)
    await message.answer("Ushbu kursning qaysi elementini o'zgartirasiz: ", reply_markup=ad_uzg)
    await AdminData.kurs_name_ust.set()
    

@dp.message_handler(state=AdminData.kurs_name_ust)
async def k_ust(message: types.Message, state: FSMContext):
    await state.update_data(kurs_name_ust=message.text)
    data = await state.get_data()
    name = data.get("kurs_name")
    ust = data.get("kurs_name_ust")
    if ust == "kursni o'chirish":
        db.delete_kurs_by_name(name)
        await message.answer("Kurs o'chirildi! ", reply_markup=admin)
        await state.finish()
        await  state.reset_state()
      
    else:
        await message.answer("Yangi ma'lumotni kiriting: ", reply_markup=types.ReplyKeyboardRemove())
        await AdminData.kurs_new_inf.set()
    
    
    
    
    
@dp.message_handler(state=AdminData.kurs_new_inf)
async def k_new_inf(message: types.Message, state: FSMContext):
    await state.update_data(kurs_new_inf=message.text)
    data = await state.get_data()
    name_ = data.get("kurs_name")
    ust_ = data.get("kurs_name_ust")
    new_ = data.get("kurs_new_inf")
    
    
    
    db.update_kurs_by_name(ust_, new_, name_)
    await message.answer("Ma'lumot o'zgartirildi! ", reply_markup=admin)
    await state.finish()
    await  state.reset_state()
    


@dp.message_handler(text="E'lon berish")
async def elon_nom(message: types.Message):
    await message.answer("E'lon uchun rasm yuboring: ", reply_markup=types.ReplyKeyboardRemove())
    await AdminRecData.rekl_rasm.set()
    
    
    
@dp.message_handler(content_types="photo", state=AdminRecData.rekl_rasm)
async def raqam(message: types.Message, state: FSMContext):  
    foto = message.photo[-1].file_id
    await state.update_data(rekl_rasm=foto)
    await message.answer("E'lon uchun matn kiriting:")
    await AdminRecData.rekl_text.set()
  
    
@dp.message_handler(state=AdminRecData.rekl_text)
async def raqam(message: types.Message, state: FSMContext):
    await state.update_data(rekl_text=message.text)
    await message.answer("Reklama ushun knopka tanlang: ", reply_markup= await reklama())
    await AdminRecData.rekl_knopka.set()
    

@dp.callback_query_handler(text="knopka_yoz", state= AdminRecData.rekl_knopka)
async def raqam(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(rekl_knopka=call.data[-1])
    # data1 = call.data[-1]
    
    # print(data1)
    data = await state.get_data()
    photo_ = data.get("rekl_rasm")  
    text_ = data.get("rekl_text")
    await call.message.answer_photo(photo=photo_, caption=text_, reply_markup=await kurs_yoz_btn())
    await call.message.answer("⬆️ Yuqoridagi ma'lumotlarni tasdiqlaysizmi", reply_markup=tasdiq_admin_rek)
    await AdminRecData.rekl_tasdiq.set()



@dp.callback_query_handler(text="url", state= AdminRecData.rekl_knopka)
async def raqam(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(rekl_knopka=call.data[-1])
    await call.message.answer("URL knopka uchun text kiriting: ", reply_markup=types.ReplyKeyboardRemove())
    await AdminRecData.rekl_url_text.set()
    
    
@dp.message_handler(state=AdminRecData.rekl_url_text)
async def url(message: types.Message, state: FSMContext):
    await state.update_data(rekl_url_text=message.text)
    await message.answer("URL manzilni kiriting: ")
    await AdminRecData.rekl_url_manz.set()
    
@dp.message_handler(state=AdminRecData.rekl_url_manz)
async def url(message: types.Message, state: FSMContext):
    await state.update_data(rekl_url_manz=message.text)
    await message.answer("URL manzilni kiriting: ")
    
    data = await state.get_data()
    print(data)
    photo_ = data.get("rekl_rasm")  
    text_ = data.get("rekl_text")
    url_text = data.get("rekl_url_text")
    url_manz = data.get("rekl_url_manz")
    print(url_manz)
    info = f"""
    {text_}
    
    {url_text}
    
    {url_manz}
    """
    await message.answer_photo(photo=photo_, caption=info)
    await message.answer("⬆️ Yuqoridagi ma'lumotlarni tasdiqlaysizmi", reply_markup=tasdiq_admin_rek)
    await AdminRecData.rekl_tasdiq.set()
    
    
 
@dp.callback_query_handler(text="bez_knopka", state= AdminRecData.rekl_knopka)
async def raqam(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(rekl_knopka=call.data[-1])
    data = await state.get_data()
    photo_ = data.get("rekl_rasm")  
    text_ = data.get("rekl_text")
    await call.message.answer_photo(photo=photo_, caption=text_)
    await call.message.answer("⬆️ Yuqoridagi ma'lumotlarni tasdiqlaysizmi", reply_markup=tasdiq_admin_rek)
    await AdminRecData.rekl_tasdiq.set()
    
    


@dp.callback_query_handler(text="ha_adm_rek", state=AdminRecData.rekl_tasdiq)
async def raqam(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo_ = data.get("rekl_rasm")
    text_ = data.get("rekl_text")
    users = db.select_users()
    spam = 0
    no_spam = 0
    
    
    
    for user in users:
              
        user_ = user
        try:
            await bot.send_photo(chat_id=user_[0], photo=photo_, caption=text_, reply_markup=await kurs_yoz_btn())
            no_spam+=1
        except:
            spam+=1

    await call.message.answer("Reklama yuborildi", reply_markup=admin)
    info = f"Xabar yetib borgan foydalanuvchilar: {no_spam} ta \n\nXabar yetib bormagan foydalanuvchilar: {spam} ta"
    await bot.send_message(ADMIN, info)
    await state.finish()
    await state.reset_state()
    


@dp.callback_query_handler(text="yo'q_adm_rek", state=AdminRecData.rekl_tasdiq)
async def raqam(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Reklama o'chirildi", reply_markup=admin)
    await state.finish()
    await state.reset_state()





   
# ============================= kursga yozilish =======================================================


@dp.callback_query_handler(text="yoz")
async def roy_ot(call:types.CallbackQuery):
    await call.message.answer("To'liq ismingizni yuboring: ", reply_markup=types.ReplyKeyboardRemove())
    await UserInfoData.state_name.set()


@dp.message_handler(state=UserInfoData.state_name)
async def welcome(message: types.Message, state: FSMContext):
    await state.update_data(state_name=message.text)
    await message.answer("yoshingizni kiriting: ", reply_markup=types.ReplyKeyboardRemove())
    await UserInfoData.state_age.set()
    




@dp.message_handler(state=UserInfoData.state_age)
async def agee(message: types.Message, state: FSMContext):
    await state.update_data(state_age=message.text)
    markup = await kurs_button()
    await message.answer("Kursni tanlang: ", reply_markup=markup)
    await UserInfoData.state_kurs.set()




@dp.message_handler(state=UserInfoData.state_kurs)
async def number(message: types.Message, state: FSMContext):
    await state.update_data(state_kurs=message.text)
    await message.answer("Telefon raqamingizni yuboring: ", reply_markup=cont)
    await UserInfoData.state_phone_number.set()


@dp.message_handler(content_types="contact", state=UserInfoData.state_phone_number)
async def raqam(message: types.Message, state: FSMContext):
    contact_ = message.contact["phone_number"]
    await state.update_data(state_phone_number=contact_)
    photo = open("images/1.jpg", "rb")
    data = await state.get_data()
    name_ = data.get("state_name")
    age_ = data.get("state_age")
    kurs_ = data.get("state_kurs")
    info = f"""
    
    F.I.O: {name_}
    Yoshi: {age_} da
    Kurs: {kurs_}
    Telefon raqami: {contact_}
    
    Ushbu ma'lumotlar to'g'riligini tasdiqlaysizmi?
    """
    
    await message.answer_photo(photo=photo, caption=info, reply_markup=tasdiq)
    await UserInfoData.state_check.set()
    


@dp.callback_query_handler(text="ha", state=UserInfoData.state_check)
async def cheek(call:types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ma'lumotlaringiz qabul qilindi! ", reply_markup=menu)
    
    
    data_ = await state.get_data()
    name1 = data_.get("state_name")
    age1 = data_.get("state_age")
    kurs1 = data_.get("state_kurs")
    number = data_.get("state_phone_number")
    
    
    info1 = f"""
    Yangi foydalanuvchi: 
    F.I.O: {name1}
    Yoshi: {age1} da
    Kurs: {kurs1}
    Telefon raqami: {number}
    """
    
    
    await bot.send_message(ADMIN, info1)
    await state.finish()
    await state.reset_state()
    



@dp.callback_query_handler(text="yo'q", state=UserInfoData.state_check)
async def yakun(call:types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ma'lumotlaringiz o'chirildi!", reply_markup=menu)
    
    
    await state.finish()
    await state.reset_state()

# ========================= filiallar ===============================================

@dp.callback_query_handler(text="o'q mark")
async def filialla(call:types.CallbackQuery):
    info = "Bizning filiallarimiz: "
    photo = open("images/2.jpg", "rb")
    markup = await filiallar()
    
    await call.message.answer_photo(photo=photo, caption=info, reply_markup=markup)



@dp.callback_query_handler(Text(startswith=f"filiallar_"))
async def fil(call:types.CallbackQuery):
    data1 = call.data[-1]
    markup = await filial()
    data = Database()
    info = data.select_filial(data1)
    inf = info[2]
    belgi = inf.index(" ")
    latitude = inf[:belgi]
    longitude = inf[belgi+1: ]
    await call.message.answer_location(latitude=latitude, longitude=longitude, reply_markup=markup)






@dp.callback_query_handler(text="fil_ort")
async def fil_ort(call:types.CallbackQuery):
    info = "Bizning filiallarimiz: "
    photo = open("images/2.jpg", "rb")
    markup = await filiallar()
    await call.message.answer_photo(photo=photo, caption=info, reply_markup=markup)



@dp.callback_query_handler(text="fillar_ort")
async def ch_fil(call:types.CallbackQuery):
    await call.message.answer("👋 Salom! IT-LABS Dasturlash Akademiyasi aloqada", reply_markup=menu)



# =============================== information =================================================

@dp.callback_query_handler(text="bog'lan")
async def malumot(call:types.CallbackQuery):
    await call.message.answer("Qo'shincha savollar va takliflar uchun telefon: \n\n+998950303036", reply_markup=ortga_m)




@dp.callback_query_handler(text="mal_ort")
async def ch_fil(call:types.CallbackQuery):
    await call.message.answer("👋 Salom! IT-LABS Dasturlash Akademiyasi aloqada", reply_markup=menu)



# ========================== kurslar ro'yxati ===============================================

@dp.callback_query_handler(text="biz kurs")
async def kurs(call:types.CallbackQuery):
    info = "Bizning kurslarimiz: "
    photo = open("images/2.jpg", "rb")
    markup = await kurslar_()
    await call.message.answer_photo(photo=photo, caption=info, reply_markup=markup)
    






@dp.callback_query_handler(Text(startswith=f"Kurslar_"))
async def kurs(call:types.CallbackQuery):
    int = call.data.index("_")
    id = call.data[int+1:]
    kurs = db.select_kurs(id)
    info = f"""
{kurs[1]}
    
⏰ Dars vaqti: {kurs[2]}

📅 Kurs davomiyligi: {kurs[3]}

💸 Kurs narxi oyiga {kurs[4]} so'm

Nimalarni o‘rgatamiz ?:

{kurs[5]}

📌Kurs davomida shaxsiy portfoilo yaratasiz. 

🚀Darslarda 100% amaliy bilimlarga ega bo'lasiz.
    """

    
    
    await call.message.answer_photo(photo=kurs[6], caption=info, reply_markup=kurs_menus)




@dp.callback_query_handler(text="kurs_yozl")
async def ch_fil(call:types.CallbackQuery):
    await call.message.answer("To'liq ismingizni yuboring: ", reply_markup=types.ReplyKeyboardRemove())
    await UserInfoData.state_name.set()



@dp.callback_query_handler(text="kurslar_ort")
async def ch_fil(call:types.CallbackQuery):
    info = "Bizning kurslarimiz: "
    photo = open("images/2.jpg", "rb")
    markup = await kurslar_()
    await call.message.answer_photo(photo=photo, caption=info, reply_markup=markup)






@dp.callback_query_handler(text="kurslarga_yoz")
async def ch_fil(call:types.CallbackQuery):
    await call.message.answer("To'liq ismingizni yuboring: ", reply_markup=types.ReplyKeyboardRemove())
    await UserInfoData.state_name.set()



@dp.callback_query_handler(text="biz_kurs_ort")
async def ch_fil(call:types.CallbackQuery):
    info = "Bizning kurslarimiz: "
    photo = open("images/2.jpg", "rb")
    await call.message.answer_photo(photo=photo, caption=info, reply_markup=menu)







@dp.message_handler(content_types="photo")
async def raqam(message: types.Message):  
    photo = message.photo[-1].file_id
    print(photo)
    




# @dp.message_handler(content_types='location')
# async def exo(message: types.Message):
#     latitude = message.location['latitude']
#     longitude = message.location['longitude']
#     print(latitude, longitude)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
