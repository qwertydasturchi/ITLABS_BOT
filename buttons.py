from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from baza import Database
db = Database()




menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏢 O'quv markazlarimiz", callback_data="o'q mark"),
            InlineKeyboardButton(text="📙 Bizning kurslar", callback_data = "biz kurs")
        ],
        [
            InlineKeyboardButton(text="📞 Biz bilan bog'lanish", callback_data="bog'lan"),
            InlineKeyboardButton(text="📌 Kursga yozilish", callback_data="yoz")
        ],
    ]
)




async def kurs_button():
    
    
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    kurslar = db.select_kurslar()
   
    for i in kurslar:
        button.add(KeyboardButton(text=i[1]))
    
    return button




async def kurslar_():
    
    button = InlineKeyboardMarkup(resize_keyboard=True)
    kurslar = db.select_kurslar()
    
   
    for kurs in kurslar:
        button.add(InlineKeyboardButton(text=kurs[1], callback_data=f"Kurslar_{kurs[0]}"))
    button.add(InlineKeyboardButton(text="📌 Kursga yozilish", callback_data="biz_kurs_yoz"))
    button.add(InlineKeyboardButton(text="⬅️ Ortga", callback_data="biz_kurs_ort"))   
    return button







cont = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton("Telefon raqamni yuborish", request_contact=True,)
        ]
    ], resize_keyboard=True
)



tasdiq = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="ha"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="yo'q")
        ]
    ]
)







# filiallar = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="🏢 Chilonzor filiali", callback_data="chil")
#         ],
#         [
#             InlineKeyboardButton(text="🏢 Beruniy filiali", callback_data="ber")
#         ],
#         [
#             InlineKeyboardButton(text="⬅️ Ortga", callback_data="flar_ort")
#         ]
#     ]
# )




async def filiallar():
    button = InlineKeyboardMarkup(resize_keyboard=True)
    fillar = db.select_filiallar()
    for i in fillar:
        button.add(InlineKeyboardButton(text=i[1], callback_data=f"filiallar_{i[0]}"))
    button.add(InlineKeyboardButton(text="⬅️ Ortga", callback_data="fillar_ort"))
    
    return button


async def filial():
    button = InlineKeyboardMarkup(resize_keyboard=True)
    
    
    
    button.add(InlineKeyboardButton(text="Ortga", callback_data="fil_ort"))
    
    return button







f_l_ortga = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="fil_ort")
        ]
    ]
)



ortga_m = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="mal_ort")
        ]
    ]
)






kurs_menus = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Kursga yozilish", callback_data="kurslarga_yoz")
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="kurslar_ort")
        ]
    ]
)





####################  Admin   ##########################



admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Kurs qo'shish"),
            KeyboardButton("Kurslarni yangilash / o'chirirsh")
        ],
        [
            KeyboardButton("E'lon berish")
        ]
    ], resize_keyboard=True
)



tasdiq_admin_kurs = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="ha_adm"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="yo'q_adm")
        ]
    ]
)






kurs_tahlil = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Kursni o'chirish", callback_data="kurs_och")
        ],
        [
            InlineKeyboardButton(text=" Kurs ma'lumotlarini qayta kiritish", callback_data="kurs_ooch")
        ]
    ], 
)


ad_uzg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="nomi"),
            KeyboardButton(text="vaqti")
        ],
        [
            KeyboardButton(text="davomiyligi"),
            KeyboardButton(text="narxi")
        ],
        [
            KeyboardButton(text="dicription"),
            KeyboardButton(text="photo")
        ],
        [
            KeyboardButton(text="kursni o'chirish")
        ]
        
        ], resize_keyboard=True
)


#########################   reklama     ######################




# reklama = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Kursga yozilish", callback_data="knopka_yoz"),
#             InlineKeyboardButton(text="URL", callback_data="url")
#         ],
#         [
#             InlineKeyboardButton(text="knopkasiz", callback_data="bez_knopka")
#         ]
#     ]
# )

async def reklama():
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text="Kursga yozilish", callback_data="knopka_yoz"), InlineKeyboardButton(text="URL", callback_data="url"))
    button.add(InlineKeyboardButton(text="knopkasiz", callback_data="bez_knopka"))
    return button


async def kurs_yoz_btn():
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text="📌 Kursga yozilish", callback_data="biz_kurs_yoz"))
    return button



tasdiq_admin_rek = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="ha_adm_rek"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="yo'q_adm_rek")
        ]
    ]
)