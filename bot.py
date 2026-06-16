import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7406318604:AAGonyOcJPVUzawdS_BPXJDZe4enKajKrQg")

# ================================================================
# ПОЛНАЯ БАЗА ЗНАНИЙ — RENEW + CARELIKA + LARIMIDE
# ================================================================

RENEW_PROTOCOLS = {
    "купероз": {
        "title": "🌿 АНТИКУПЕРОЗНАЯ ТЕРАПИЯ «SENSITIVE CARE»",
        "brand": "RENEW",
        "info": "Показания: купероз, реактивная и чувствительная кожа\nПериодичность: 1 раз в 7–14 дней, курс 5–10 процедур\nСебестоимость: ~3,1€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Gentle Eye&Lip Make-Up Remover",
            "2️⃣ ОЧИЩЕНИЕ — Cleanser for Dry & Normal Skin",
            "3️⃣ ТОНИЗАЦИЯ — Hydrofresh Lotion",
            "4️⃣ ЭКСФОЛИАЦИЯ — AHA Refreshing Exfoliator",
            "5️⃣ ТОНИЗАЦИЯ — AHA & BHA Lotion (подготовка к пилингу)",
            "6️⃣ ПИЛИНГ — Redness Gentle Peel pH 3,5 — 5–10 мин, холодная вода",
            "7️⃣ КОНЦЕНТРАТ — Redness Concentrate",
            "8️⃣ МАСКА — Redness Mask — 15 мин",
            "9️⃣ ФИНИШ — Eye Contour Cream\n   Лето: Moisturizing Cream Vitamin C SPF-25\n   Зима: Restructuring Cream"
        ],
        "homecare": {
            "morning": [
                "Очищение: Cleanser Dry Normal или Dermo Control Cleansing Gel",
                "Тонизация: Hydrofresh Lotion",
                "Глаза: Eye Contour Cream",
                "Крем: Moisturizing Cream Oily SPF-15 (жирная) / Moisturizing Cream Vitamin C SPF-25 (сухая)"
            ],
            "evening": [
                "Очищение: тот же гель",
                "Тонизация: Hydrofresh Lotion",
                "Сыворотка: Redness Concentrate",
                "Глаза: Eye Contour Cream",
                "Крем: Redness Balm"
            ]
        },
        "crossbrand": {
            "CARELIKA": [
                "Hydra Infusion Mask — вместо Redness Mask, глубокое увлажнение без раздражения",
                "Algae Peel Off Mask Cryogenic Complex — криогенный эффект, сужает сосуды",
                "Filler Elegance Correction Face Cream (pH 5,0–6,0) — деликатный финишный крем"
            ]
        }
    },
    "акне": {
        "title": "🧴 ЛЕЧЕБНЫЙ УХОД ЗА ПРОБЛЕМНОЙ КОЖЕЙ",
        "brand": "RENEW",
        "info": "Показания: акне 1–2 ст., постакне, воспаления\nПериодичность: 1 раз в неделю, курс 10 процедур\nСебестоимость: ~2,5€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Gentle Eye&Lip Make-Up Remover",
            "2️⃣ ОЧИЩЕНИЕ — Deep Lathering Abstergent pH 3,5–4,5",
            "3️⃣ ТОНИЗАЦИЯ — Complex Peel Solution",
            "4️⃣ ЭКСФОЛИАЦИЯ — Cream Peeling Gommage",
            "5️⃣ ТОНИЗАЦИЯ — Complex Peel Solution (подготовка к пилингу)",
            "6️⃣ ПИЛИНГ — AHA Peeling — 5 мин",
            "7️⃣ МАСКА — Dermo Control Mask — 15 мин",
            "8️⃣ МАСКА — Charcoal Soothing Mask или Gentle Mask Passiflora",
            "9️⃣ ТОНИЗАЦИЯ — Dermo Control Lotion / Hydrofresh Lotion",
            "🔟 ФИНИШ — Triple Active Day Cream SPF-15"
        ],
        "homecare": {
            "morning": [
                "Очищение: Deep Lathering Abstergent",
                "Тонизация: Dermo Control Lotion (жирная) / Hydrofresh Lotion (норм/сухая)",
                "Глаза: Eye Contour Cream",
                "Крем: Triple Active Day Cream SPF-15"
            ],
            "evening": [
                "Очищение: Deep Lathering Abstergent",
                "Тонизация: Complex Peel Solution (каждый вечер)",
                "Глаза: Eye Contour Cream",
                "Крем: Multifunctional Accelerative Cream / Make-Up Treatment Cream",
                "Локально: Drying Treatment или Spot Local Gel"
            ]
        },
        "crossbrand": {
            "CARELIKA": [
                "Skin Chat Derma Spiq Peel 7% — спикулы создают 3 млн микроканалов, усиливают проникновение активных",
                "TXG Complex Depigmenting Cocktail — работает с постакне пигментацией",
                "Biocellulose Face Mask Oxygen — глубокое восстановление после процедуры",
                "Amber Carboxy Therapy Mask — регулирует жирность и уменьшает воспаление"
            ]
        }
    },
    "пигментация": {
        "title": "✨ ОТБЕЛИВАЮЩАЯ ТЕРАПИЯ «STOP PIGMENT»",
        "brand": "RENEW",
        "info": "Показания: пигментные пятна, неровный тон\nПериодичность: 1 раз в 7–14 дней, курс 10 процедур\nСебестоимость: ~3,1€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Gentle Eye&Lip Make-Up Remover",
            "2️⃣ ОЧИЩЕНИЕ — Multifruit Peel Soap (просушить!)",
            "3️⃣ ТОНИЗАЦИЯ — AHA & BHA Lotion",
            "4️⃣ ЭКСФОЛИАЦИЯ — Cream Peeling Gommage",
            "5️⃣ ПИЛИНГ — AHA Peeling — 5 мин",
            "6️⃣ ЛОКАЛЬНО (осень-зима) — AHA & BHA Peeling на пятна — 3–5 мин",
            "7️⃣ МАСКА — Depigmenting Mask — 15 мин",
            "8️⃣ СЫВОРОТКА — Depigmenting Serum",
            "9️⃣ МАСКА — Gentle Mask Passiflora — 20 мин",
            "🔟 ТОНИЗАЦИЯ — Hydrofresh Lotion",
            "1️⃣1️⃣ ФИНИШ — Eye Contour Cream + Sun Protect SPF-50 ❗обязателен!"
        ],
        "homecare": {
            "morning": [
                "Очищение: Multifruit Peel Soap",
                "Тонизация: Hydrofresh Lotion",
                "Глаза: Shining Eyes Vitamin C",
                "Крем: Sunscreen SPF-30 Demi Make-Up — ❗каждый день!"
            ],
            "evening": [
                "Очищение: Multifruit Peel Soap",
                "Тонизация: AHA & BHA Lotion",
                "Глаза: Eye Contour Cream",
                "Сыворотка: Depigmenting Serum",
                "Крем: Depigmenting Cream (не при беременности!)"
            ]
        },
        "crossbrand": {
            "CARELIKA": [
                "Amber Line 15in1 (янтарная кислота 2%) — мощное осветление, использовать как очищающий шаг",
                "BHA & Amber Acid Renewal Booster — под маску вместо/после Depigmenting Serum",
                "TXG Complex Depigmenting Cocktail — транексамовая кислота, 4 механизма действия на пигмент",
                "Biocellulose Face Mask Lightening — финальная маска курса",
                "Multi-Acid Peel Anti-Pigment pH 5–6 — деликатный, всесезонный"
            ]
        }
    },
    "антивозраст": {
        "title": "💎 ANTI AGE УХОД",
        "brand": "RENEW",
        "info": "Показания: морщины, птоз, возрастные изменения\nПериодичность: 1 раз в 7–14 дней, курс 5–10 процедур\nСебестоимость: ~2,9€ (лицо) / 5,3€ (лицо+шея+декольте)",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Gentle Eye&Lip Make-Up Remover",
            "2️⃣ ОЧИЩЕНИЕ — Multifruit Peel Soap",
            "3️⃣ ТОНИЗАЦИЯ — AHA & BHA Lotion",
            "4️⃣ ПИЛИНГ (адаптированная кожа) — AHA & BHA Peeling — 1 мин",
            "5️⃣ МАССАЖ — Massage Multivitamin Serum — до 30 мин",
            "6️⃣ ТОНИЗАЦИЯ — Hydrofresh Lotion",
            "7️⃣ МАСКА — Anti Aging Firming Mask — 15 мин",
            "8️⃣ ТОНИЗАЦИЯ — Hydrofresh Lotion",
            "9️⃣ СЫВОРОТКА — Intense Skin Revitalizer Q10",
            "🔟 ФИНИШ — Restoring Eye Cream + Aqua Vital Revitalizing Cream SPF-22\n    Шея/декольте: Neck & Decollete Firming Cream"
        ],
        "homecare": {
            "morning": [
                "Очищение: Cleanser Dry Normal",
                "Тонизация: PHA Refining Skin Tonic",
                "Глаза: Restoring Eye Cream",
                "Сыворотка: Intense Skin Revitalizer (+ самомассаж 10 мин)",
                "Крем: Aqua Vital Revitalizing Cream SPF-22"
            ],
            "evening": [
                "Очищение: Cleanser Dry Normal",
                "Тонизация: PHA Refining Skin Tonic",
                "Сыворотка: Intense Skin Revitalizer",
                "Глаза: Restoring Eye Cream",
                "Крем: Energy Refill Anti Aging Cream"
            ]
        },
        "crossbrand": {
            "CARELIKA": [
                "Thermo Modeling Gypsum Mask — мощный лифтинг, моделирование контура после массажа",
                "Orchid Stem Cell Fluid Serum — фитостволовые клетки, под Anti Aging Firming Mask",
                "Caviar Serum — коллаген и лифтинг, до наложения маски",
                "Oligopeptide Anti-Age Serum — пептиды, альтернатива Intense Skin Revitalizer",
                "Algae Peel Off Mask Algi Twin — финишный моделирующий шаг"
            ]
        }
    },
    "увлажнение": {
        "title": "💧 АКВА-ЛИФТИНГ И ЭКСТРА-УВЛАЖНЕНИЕ",
        "brand": "RENEW",
        "info": "Показания: сухая, обезвоженная, тусклая кожа\nПериодичность: 1 раз в 7–10 дней, курс 5–10 процедур\nСебестоимость: ~1,9€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Gentle Eye&Lip Make-Up Remover",
            "2️⃣ ОЧИЩЕНИЕ — Fresh Calming Skin Foam",
            "3️⃣ ТОНИЗАЦИЯ — PHA Refining Skin Tonic",
            "4️⃣ ЭКСФОЛИАЦИЯ — Soft Peeling Gel — 1–2 мин",
            "5️⃣ ТОНИЗАЦИЯ — PHA Refining Skin Tonic",
            "6️⃣ МАСКА — Skin Repair Moisturizing Mask — 10–15 мин",
            "7️⃣ ТОНИЗАЦИЯ — PHA Refining Skin Tonic",
            "8️⃣ СЫВОРОТКА — Dew Drops HA",
            "9️⃣ ФИНИШ — Eye Contour Gel + Hydro Comfort Glow Moisturizer SPF-25"
        ],
        "homecare": {
            "morning": [
                "Очищение: Fresh Calming Skin Foam",
                "Тонизация: PHA Refining Skin Tonic",
                "Глаза: Eye Contour Gel",
                "Крем: Hydro Comfort Glow Moisturizer SPF-25"
            ],
            "evening": [
                "Очищение: Fresh Calming Skin Foam",
                "Тонизация: PHA Refining Skin Tonic",
                "Глаза: Eye Contour Gel",
                "Крем: Antistress Nourishing Cream"
            ]
        },
        "crossbrand": {
            "CARELIKA": [
                "Hydra Infusion Mask — интенсивное увлажнение, заменить или дополнить Skin Repair Mask",
                "Hydration Boost Marine Serum — морской гиалурон, под маску вместо Dew Drops",
                "Unique Hyaluronic Booster (с Matrixyl 3%) — бустер гиалурона + пептиды",
                "Softening Aloe Vera Gel — гель под плёнку, альтернатива Aloevend Gel"
            ]
        }
    }
}

CARELIKA_PROTOCOLS = {
    "янтарная карбокситерапия": {
        "title": "🟡 ЯНТАРНАЯ КАРБОКСИТЕРАПИЯ",
        "brand": "CARELIKA",
        "info": "Показания: зрелая комбинированная кожа, акне, тусклость, пигментация\nКурс: 5–10 процедур, 1 раз в неделю\nСебестоимость: ~6,54€ · Цена: 95€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Silky Cleansing Milk with Cotton Extract (2 мл)",
            "2️⃣ ОЧИЩЕНИЕ — Amber Therapy Cleansing Powder (1 г + вода → пена, 1–2 мин)",
            "3️⃣ ТОНИЗАЦИЯ — Amber Brightening Toner 15in1 (2 мл)",
            "4️⃣ СЫВОРОТКА — BHA & Amber Acid Renewal Booster (2 мл) — не смывать",
            "5️⃣ МАСКА — Amber Carboxy Therapy Mask (20 г + 15 мл воды → пена) — 15 мин, смыть",
            "6️⃣ МАСКА — Amber 15in1 Gel Mask (5 мл) — 15 мин (+ гуаша или фонофорез)",
            "7️⃣ ТОНИЗАЦИЯ — Amber Brightening Toner 15in1 (2 мл)",
            "8️⃣ ФИНИШ — Amber 15in1 Cream (1 мл)"
        ],
        "homecare": {
            "morning": ["Amber Exfoliating Cleanser 15in1", "Amber Brightening Toner 15in1", "Amber Brightening Serum 15in1", "Amber Cream 15in1 + SPF"],
            "evening": ["Amber Exfoliating Cleanser 15in1", "Amber Brightening Toner 15in1", "Amber Brightening Serum 15in1", "Amber Cream 15in1"]
        },
        "crossbrand": {
            "RENEW": [
                "Депигментирующая сыворотка RENEW Depigmenting Serum (альфа-арбутин) — после Amber Booster",
                "RENEW Redness Mask — добавить при куперозе после Amber маски",
                "RENEW Moisturizing Cream Vitamin C SPF-25 — финишный крем вместо Amber Cream"
            ]
        }
    },
    "орхидея": {
        "title": "🌸 ТЕРАПИЯ СТВОЛОВЫМИ КЛЕТКАМИ ОРХИДЕИ",
        "brand": "CARELIKA",
        "info": "Показания: птоз, морщины, потеря эластичности, тусклость\nПериодичность: 1 раз в 7–10 дней, курс от 5 процедур\nСебестоимость: ~4,82€ · Цена: 100€",
        "steps": [
            "1️⃣ ОЧИЩЕНИЕ — Orchid Stem Cell Cleansing Milk (2 мл)",
            "2️⃣ ТОНИЗАЦИЯ — Orchid Stem Cell Toning Lotion (2 мл)",
            "3️⃣ ЭКСФОЛИАЦИЯ — Gentle Particle-Free Scrub with AHA (4 мл)",
            "4️⃣ МАСКА — Orchid Stem Cell Cream Mask (3 мл) — 15 мин",
            "5️⃣ АЛЬГИНАТ — Algae Peel Off Mask Caviar Extract (25 г + 70 мл воды) — 15–20 мин",
            "6️⃣ ТОНИЗАЦИЯ — Orchid Stem Cell Toning Lotion (2 мл)",
            "7️⃣ СЫВОРОТКА — Orchid Stem Cell Fluid Serum (1 мл) — щипковый массаж 5–7 мин",
            "8️⃣ ГЛАЗА — Orchid Stem Cell Eye Contour Serum (0,5 мл)",
            "9️⃣ ФИНИШ — Orchid Stem Cell Cream Anti-aging (1 мл)"
        ],
        "homecare": {
            "morning": ["Orchid Stem Cell Cleansing Milk", "Orchid Stem Cell Toning Lotion", "Orchid Stem Cell Fluid Serum", "Orchid Stem Cell Eye Contour Serum", "Orchid Stem Cell Cream Anti-aging"],
            "evening": ["Orchid Stem Cell Cleansing Milk", "Orchid Stem Cell Toning Lotion", "Orchid Stem Cell Fluid Serum", "Orchid Stem Cell Eye Contour Serum", "Orchid Stem Cell Cream Anti-aging"]
        },
        "crossbrand": {
            "RENEW": [
                "RENEW Intense Skin Revitalizer (Q10 + бакучиол) — под или после Orchid Serum",
                "RENEW Berry Lift Alginate Mask — вместо Algae Caviar маски",
                "RENEW Aqua Vital Revitalizing Cream SPF-22 — финишный крем с Matrixyl + SPF"
            ]
        }
    },
    "гипсовая": {
        "title": "🗿 СКУЛЬПТУРНАЯ ГИПСОВАЯ ТЕРАПИЯ",
        "brand": "CARELIKA",
        "info": "Показания: птоз, дряблость, отечность\nКурс: 5–10 процедур\nСебестоимость: ~12,02€ · Цена: 110€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Silky Cleansing Milk (2 мл)",
            "2️⃣ ОЧИЩЕНИЕ — SOS Cleansing Powder + Niacinamide (1 г + вода, 1–2 мин)",
            "3️⃣ ТОНИЗАЦИЯ — Toning Lotion (2 мл)",
            "4️⃣ СЫВОРОТКА — Caviar Serum (1 мл)",
            "5️⃣ МАСКА — Hydra Infusion Mask ИЛИ Orchid Stem Cell Cream Mask (3 мл) + марля",
            "6️⃣ ГИПСОВАЯ МАСКА — Thermo Modeling Gypsum Mask (220 г + 110 мл воды) — 30 мин поверх марли",
            "7️⃣ SPA ДЛЯ РУК — Exotic Body Scrub + Exotic Body Butter (пока маска)",
            "8️⃣ ТОНИЗАЦИЯ — Toning Lotion (2 мл)",
            "9️⃣ СЫВОРОТКА — Oligopeptide Anti-Age / Hydration Boost Marine / Collagen Elastin (1 мл)",
            "🔟 ФИНИШ — Filler Elegance Face Cream ИЛИ Amber 15in1 Cream + Eye Cream + Lip Cream"
        ],
        "homecare": {
            "morning": ["Toning Lotion", "Oligopeptide Anti-Age Serum", "Filler Elegance Eye Cream", "Filler Elegance Face Cream + SPF"],
            "evening": ["Toning Lotion", "Orchid Stem Cell Fluid Serum", "Filler Elegance Eye Cream", "Filler Elegance Face Cream"]
        },
        "crossbrand": {
            "RENEW": [
                "RENEW Intense Skin Revitalizer (Q10) — вместо Caviar Serum на шаге 4",
                "RENEW Dew Drops HA — гиалурон после снятия гипсовой маски",
                "RENEW Aqua Vital Revitalizing Cream SPF-22 — финиш с Matrixyl + SPF"
            ]
        }
    },
    "derma spiq": {
        "title": "⚡ SKIN CHAT DERMA SPIQ PEEL",
        "brand": "CARELIKA",
        "info": "Показания: акне 1–2 ст., постакне, рубцы, пористая кожа, пигментация\nПериодичность: 1 раз в 7–10 дней, курс 3–6 процедур\nСебестоимость: ~16,91€ · Цена: 110€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Silky Cleansing Milk (2 мл)",
            "2️⃣ ОЧИЩЕНИЕ — Amber Exfoliating Cleanser 15in1 (2 мл)",
            "3️⃣ ТОНИЗАЦИЯ — Amber Brightening Toner 15in1 (2 мл)",
            "4️⃣ СПИКУЛЫ — Skin Chat Derma Spiq Peel 7% (3 мл) — лёгкими движениями на сухую кожу, 3 мин ❗Не тереть!",
            "5️⃣ КОКТЕЙЛЬ — TXG Complex (пигмент) / Exovital (омоложение) / Lumiderm (антиоксидант) — 1 мл, не смывать",
            "6️⃣ МАСКА — Biocellulose Face Mask: Lightening / Blueberry / Collagen / Oxygen — 20–30 мин",
            "7️⃣ ФИНИШ — Skin Chat Soothing & Repair Cream (2 мл) + Filler Elegance Eye + Lip Cream"
        ],
        "homecare": {
            "morning": ["Amber Exfoliating Cleanser 15in1", "Amber Brightening Toner 15in1", "Filler Elegance Eye Cream", "Skin Chat Soothing & Repair Cream + SPF"],
            "evening": ["Amber Exfoliating Cleanser 15in1", "Amber Brightening Toner 15in1", "TXG / Exovital / Lumiderm Complex (по проблеме)", "Skin Chat Soothing & Repair Cream"]
        },
        "crossbrand": {
            "RENEW": [
                "RENEW AHA & BHA Lotion — вместо Amber Toner на шаге 3 (более активная подготовка)",
                "RENEW Depigmenting Serum — после TXG коктейля для двойного осветляющего эффекта",
                "RENEW Gentle Mask Passiflora — вместо Biocellulose при чувствительной коже",
                "RENEW Restructuring Cream — финиш для барьерного восстановления"
            ]
        }
    },
    "неинвазивная карбокситерапия": {
        "title": "🫧 НЕИНВАЗИВНАЯ КАРБОКСИТЕРАПИЯ",
        "brand": "CARELIKA",
        "info": "Показания: возрастные изменения, морщины, пигментация, акне, сухая кожа\nСебестоимость: ~5,37€ · Цена: 95€",
        "steps": [
            "1️⃣ ДЕМАКИЯЖ — Silky Cleansing Milk (2 мл)",
            "2️⃣ ОЧИЩЕНИЕ — SOS Cleansing Powder (1 г + вода, 1–2 мин)",
            "3️⃣ ТОНИЗАЦИЯ — Toning Lotion (2 мл)",
            "4️⃣ КАРБОКСИ МАСКА — Carboxy Therapy Fizzing Mask (20 г + 15 мл воды) — 15 мин, снять лопаточкой",
            "5️⃣ МАСКА — Hydra Infusion Mask (10 мл) — 15 мин",
            "6️⃣ ТОНИЗАЦИЯ — Toning Lotion (2 мл)",
            "7️⃣ ФИНИШ — Filler Elegance Face Cream (2 мл) + Lip Cream + Eye Cream"
        ],
        "homecare": {
            "morning": ["Toning Lotion", "Filler Elegance Eye Cream", "Filler Elegance Face Cream + SPF"],
            "evening": ["Toning Lotion", "Hydra Infusion Mask 1–2 р/нед", "Filler Elegance Face Cream"]
        },
        "crossbrand": {
            "RENEW": [
                "RENEW Dew Drops HA — под Hydra Infusion Mask для двойного увлажнения",
                "RENEW Aqua Vital Revitalizing Cream SPF-22 — финиш с антивозрастным эффектом + SPF"
            ]
        }
    }
}

LARIMIDE_PROTOCOLS = {
    "kojaxin": {
        "title": "💇 KOJAXIN — СИСТЕМА ПРОТИВ ВЫПАДЕНИЯ ВОЛОС",
        "brand": "LARIMIDE",
        "info": "Показания: андрогенная алопеция, послеродовое выпадение, редкие/тонкие волосы\nДля женщин и мужчин\nКлиника: 90% рост волос · 88,8% снижение выпадения · 63% результат за 15 дней",
        "steps": [
            "🏥 В САЛОНЕ (порядок):",
            "1️⃣ ШАМПУНЬ — KOJAXIN Anti-Hair Loss Shampoo",
            "2️⃣ МАСКА — KOJAXIN Anti-Hair Loss Mask",
            "3️⃣ АМПУЛЫ — KOJAXIN Ampoules — втереть в кожу головы",
            "",
            "🏠 ДОМАШНИЙ КУРС:",
            "• Ежедневно: KOJAXIN Ampoules на кожу головы",
            "• При мытье: Shampoo → Mask → Ampoules",
            "",
            "📦 ФОРМАТЫ:",
            "• START 15 (15 дней): 163,63€",
            "• INTENSIVE 45 (45 дней): 342,13€"
        ],
        "homecare": {
            "morning": ["KOJAXIN Ampoules — нанести на кожу головы, втереть, не смывать"],
            "evening": ["При мытье: KOJAXIN Shampoo → Mask → Ampoules"]
        },
        "crossbrand": {
            "RENEW": [
                "RENEW ENHAIR (Art. 1907005, 30€/5мл) — инъекционный мезококтейль для фолликулов",
                "Оптимальная схема: RENEW ENHAIR мезотерапия в салоне (курс 5 процедур) + KOJAXIN домашний уход ежедневно",
                "ENHAIR воздействует на фолликулы изнутри через инъекции, KOJAXIN — снаружи ежедневно"
            ]
        }
    }
}

KB_ANSWERS = {
    "скидка": "🏷️ ПРОГРАММА СКИДОК RENEW\n\n• Silver — от 500€/мес → скидка 5%\n• Gold — от 750€/мес → скидка 10%\n• Platin — от 1000€/мес → скидка 15%\n\n⚠️ Если скидка не использована в течение месяца — аннулируется.",
    "бонус": "💰 ПРОГРАММА БОНУСОВ RENEW\n\n5% бонус при каждой покупке от 300€.\nМожно использовать при следующем заказе — сумма продуктов по каталожной цене не должна превышать накопленный бонус.",
    "carelika": "🇫🇷 О БРЕНДЕ CARELIKA\n\n• Французская профессиональная космецевтика\n• Производство: сертифицированный завод, фармацевтические стандарты\n• 200+ продуктов и 55 видов масок · 27 стран\n• Награда китайского рынка 2024\n• Без парабенов · Без SLS · Cruelty Free\n• Представитель в Германии: RENEW Cosmetics\ninfo@renew-kosmetik.de | +49 173 172 51 80",
    "larimide": "🇪🇸 О БРЕНДЕ LARIMIDE\n\n• Испанский бренд · 100% веганский · Без отдушек\n• Продукт в портфеле: система KOJAXIN (выпадение волос)\n• Клинически протестирован (TrichoScan)",
    "renew": "🇮🇱 О БРЕНДЕ RENEW\n\n• 20+ лет в мире · 5 лет в Германии/Австрии\n• Израильская космецевтика · 50 000+ косметологов\n• Одобрено Минздравами Израиля и Германии · ISO + GMP\n• Не тестируется на животных\n• ~2€ расход → ~50€ прибыли с процедуры\n• Учебный центр в Нюрнберге · www.renew-kosmetik.de",
    "skin chat": "⚡ CARELIKA SKIN CHAT\n\n• Skin Chat Kit — 68,99€\n• Derma Spiq Peel 7% 15мл (5 лечений) — 43,62€\n• Soothing & Repair Cream 100мл — 35,20€\n\nКоктейли (выбрать по проблеме):\n• TXG Complex (пигментация) — 92€\n• Exovital Complex (омоложение) — 93,61€\n• Lumiderm Complex (антиоксидант)\n\nПринцип: спикулы создают 3 млн микроканалов за 3 мин → максимальное проникновение",
    "kojaxin": "💇 LARIMIDE KOJAXIN\n\n3 продукта: Ampoules + Shampoo + Mask\n\n• START 15 (15 дней): 163,63€\n• INTENSIVE 45 (45 дней): 342,13€\n\n90% рост волос · 88,8% снижение выпадения · 63% результат за 15 дней",
    "dermapen": "⚡ RENEW DERMAPEN M8 — 129,00€\n\n• Иглы 0,18мм · 6 скоростей · 0,25–2,5мм глубина\n• Повышает впитывание активных до 540%\n• Картриджи — 2,20€/шт (отдельно!)\n\nМезосистемы BioRepair Pro:\n• AntiAge — 97,50€\n• Illumination (пигментация) — 100,05€\n• AntiAcne — 99,00€",
}

WELCOME_MESSAGE = """👋 Привет! Я ассистент Renew Bibliothek.

Знаю всё о трёх брендах:
🇮🇱 RENEW — израильская космецевтика
🇫🇷 CARELIKA — французская космецевтика  
🇪🇸 LARIMIDE — испанский бренд (KOJAXIN)

Могу помочь с:
📋 Протоколы процедур по проблеме кожи
🏠 Схемы домашнего ухода
🔗 Кросс-брендовые комбинации
💶 Цены и артикулы
📦 Составы продуктов

Пиши на любом языке — отвечу на нём же!

Примеры запросов:
• Протокол при куперозе
• Что комбинировать при пигментации?
• Yantar Carboxytherapy CARELIKA
• Anti-Age Protokoll Renew + Carelika
• Программа скидок Gold"""

HELP_MESSAGE = """📚 Доступные темы:

🌿 ПРОТОКОЛЫ RENEW:
• купероз / Rosacea
• акне / Akne
• пигментация / Pigmentierung  
• антивозраст / Anti-Age
• увлажнение / Hydration

🇫🇷 ПРОТОКОЛЫ CARELIKA:
• янтарная карбокситерапия
• орхидея / Orchid Stem Cell
• гипсовая терапия / Gipsmaske
• derma spiq / спикулы
• неинвазивная карбокситерапия

💇 LARIMIDE:
• kojaxin / выпадение волос

💶 ЦЕНЫ: спроси "цена [название продукта]"
ℹ️ О БРЕНДЕ: спроси "о Renew" / "о Carelika" / "о Larimide"
🏷️ СКИДКИ: спроси "программа скидок" или "бонусы"
"""

def find_answer(text: str) -> str:
    q = text.lower().strip()

    # Протоколы RENEW
    renew_map = [
        (["купероз","rosacea","sensitive care","чувствительн","капилляр","сосуды"], "купероз"),
        (["акне","акne","прыщи","воспален","угри","постакне","проблемн","propio"], "акне"),
        (["пигмент","pigment","отбелива","депигмент","пятна","stop pigment","осветл"], "пигментация"),
        (["антивозраст","anti age","anti-age","anti-aging","старени","морщин","возраст","falten","лифтинг","птоз"], "антивозраст"),
        (["увлажн","hydrat","обезвожен","сухая кожа","аква-лифтинг","тусклая"], "увлажнение"),
    ]
    carelika_map = [
        (["янтарная карбокс","amber carboxy","amber карбокс"], "янтарная карбокситерапия"),
        (["орхидея","orchid","стволовые клетки орх"], "орхидея"),
        (["гипсовая","гипс терап","thermo modeling","gips","скульптурная"], "гипсовая"),
        (["derma spiq","спикулы","skin chat протокол","skin chat пилинг"], "derma spiq"),
        (["неинвазивная карбокс","carboxy fizzing","fizzing mask протокол","fizzing маска"], "неинвазивная карбокситерапия"),
    ]
    larimide_map = [
        (["kojaxin","выпадени","алопеция","волосы","волос","haarausfall"], "kojaxin"),
    ]

    is_proto = any(k in q for k in ["протокол","процедур","уход","домашний","лечени","схем","этап","шаг","комбинац","protocol","behandlung","anwendung"])

    for keys, proto_key in renew_map:
        if any(k in q for k in keys):
            if is_proto or any(k in q for k in keys[:2]):
                return format_protocol(RENEW_PROTOCOLS[proto_key])

    for keys, proto_key in carelika_map:
        if any(k in q for k in keys):
            return format_protocol(CARELIKA_PROTOCOLS[proto_key])

    for keys, proto_key in larimide_map:
        if any(k in q for k in keys):
            return format_protocol(LARIMIDE_PROTOCOLS[proto_key])

    # KB
    for key, answer in KB_ANSWERS.items():
        if key in q:
            return answer

    # Если ничего не нашли
    return "🤔 По этому запросу нет данных в базе.\n\nНапиши /help чтобы увидеть список доступных тем.\n\nЕсли нужна информация которой нет — уточни у руководителя."


def format_protocol(p: dict) -> str:
    brand = p["brand"]
    out = f"✅ {p['title']} [{brand}]\n"
    out += f"{p['info']}\n\n"
    out += f"📋 ЭТАПЫ ПРОЦЕДУРЫ [{brand}]:\n"
    out += "\n".join(p["steps"])

    if p.get("homecare"):
        out += f"\n\n🏠 ДОМАШНИЙ УХОД [{brand}]:\n"
        out += "☀️ УТРО:\n" + "\n".join(f"• {s}" for s in p["homecare"]["morning"])
        out += "\n🌙 ВЕЧЕР:\n" + "\n".join(f"• {s}" for s in p["homecare"]["evening"])

    if p.get("crossbrand"):
        for cb_brand, items in p["crossbrand"].items():
            out += f"\n\n🔗 ДОПОЛНЕНИЕ ИЗ {cb_brand}:\n"
            out += "\n".join(f"• {i}" for i in items)

    return out


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    answer = find_answer(text)
    # Telegram лимит — 4096 символов
    if len(answer) > 4000:
        parts = [answer[i:i+4000] for i in range(0, len(answer), 4000)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(answer)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
