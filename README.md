# 🐶 Мопс дя́дя Пёс (Гав, Гав!) — Автономний AI Telegram-Бот 24/7

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Aiogram" />
  <img src="https://img.shields.io/badge/Multi--LLM-Gemini%20%7C%20DeepSeek%20%7C%20GPT--4o%20%7C%20Claude-FF6F00?style=for-the-badge" alt="Multi-LLM" />
  <img src="https://img.shields.io/badge/SQLite-Async%20Memory-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Age-18%2B%20Only-red?style=for-the-badge" alt="18+" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License" />
  <a href="https://buymeacoffee.com/arpmag"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a>
  <a href="https://send.monobank.ua/jar/8HBjkw7ZT5"><img src="https://img.shields.io/badge/Monobank-Банка-black?style=for-the-badge&logo=monzo&logoColor=white" alt="Monobank" /></a>
</p>

> [!WARNING]
> **⚠️ ДИСКЛЕЙМЕР 18+ (Explicit Content):**
> Бот містить ненормативну лексику, жорсткий гумор, тюремний сленг та пародійний контент у стилі класичних треш-стрімів. Проєкт створено виключно в гумористичних та розважальних цілях для повнолітньої аудиторії (18+).

---

## 📖 Про проєкт

**«Мопс дядя Пёс»** — це інтелектуальний, високопродуктивний Telegram-бот на базі **aiogram 3** та сучасних нейромереж (**Google Gemini 2.5/Flash, DeepSeek V3, OpenAI GPT-4o, Claude 3.5 Haiku**), який відтворює культовий образ та характер легендарного українського треш-стрімера **Сергія Новіка («Мопса»)** та його продюсера **Андрія Щадила**.

Бот має глибоку базу знань про тюремний побут, колоритний суржик, реальні стрім-челенджі за донати, зашиті посилання на YouTube-архіви, інтерактивні команди та можливість повноцінної автономної роботи **у коментарях під постами Telegram-каналу 24/7 безкоштовно**.

---

## 🌟 Ключові можливості

* 🎭 **100% Живий характер без шаблонів:** Бот адаптується до контексту, володіє фірмовим суржиком (*«головы родные»*, *«желтые буквочки»*, *«в экстазе»*, *«гатить»*, *«шляпа усатая»*, *«от душы душевно в душу»*) та не повторює заїжджені фрази.
* 🥊 **Лайв-відіграш стрім-челленджів:** Миттєві сценки з криками на Щадила, звуками ударів та вимаганням донатів на м'ясо при згадці:
  * `Лось с разбега / Лось з розбігу / Королевский лось` 💥
  * `Муха` (прилипание скотчем к стене) 🪰
  * `Черепаха` (кастрюля на голове и удары половником) 🐢
  * `Пылесос / Пилосос` (присасывание шланга к лысине) 🧹
  * `Смачный лящ по лысине / Лящ с оттяжкой` 👋
  * `Пробить фанеру` (удар кулаком в душу) 🥋
  * `Шокер`, `Травмат`, `Чифир / Чифирбасить купчик`, `Донат на мясо` ⚡
* 💬 **Робота в коментарях каналу (Discussions):** Бот відповідає **виключно всередині треду коментарів**, не засмічуючи головну стрічку каналу.
* 🔄 **Каскадний Multi-LLM Роутер:** Автоматичне балансування та миттєвий фолбек при вичерпанні лімітів (Gemini ➡️ DeepSeek ➡️ GPT-4o ➡️ Claude).
* ☕ **Офлайн Vault-база:** Навіть якщо всі AI-сервери недоступні, бот відповість автентичною цитатою з локальної бази.
* 🧠 **Контекстна пам'ять на SQLite:** Запам'ятовує хід бесіди для кожного чату окремо.
* 🚀 **Працює 24/7 абсолютно безкоштовно:** Готові конфігурації для **Oracle Cloud Always Free**, Docker та systemd.

---

## 🔑 Де взяти API Ключі (100% БЕЗКОШТОВНО від А до Я)

Щоб запустити бота, вам знадобиться **Telegram Bot Token** та як мінімум **безкоштовний ключ Gemini API**.

### 1. Telegram Bot Token (Безкоштовно)
1. Відкрийте Telegram і знайдіть офіційного бота [@BotFather](https://t.me/BotFather).
2. Натисніть `/start` і відправте команду `/newbot`.
3. Введіть назву бота (наприклад, `Мопс дядя Пёс`).
4. Введіть юзернейм бота, що закінчується на `bot` (наприклад, `mops_my_stream_bot`).
5. `@BotFather` надішле вам токен вигляду `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ_example`. Збережіть його в `BOT_TOKEN`.

### 2. Google Gemini API Key (100% Безкоштовно, без прив'язки картки)
1. Перейдіть на [Google AI Studio](https://aistudio.google.com/).
2. Увійдіть у свій Google-акаунт.
3. Натисніть **«Get API key»** ➔ **«Create API key»**.
4. Скопіюйте створений ключ (починається на `AIzaSy...`).
5. Вставте його в `GEMINI_API_KEY`. Google надає **безкоштовний тариф із високими лімітами запитів на день**!

### 3. Як дізнатися свій ADMIN_ID та ALLOWED_CHATS
1. Відкрийте бота [@userinfobot](https://t.me/userinfobot) — він покаже ваш числовий Telegram ID (наприклад, `123456789`). Запишіть його в `ADMIN_IDS`.
2. Щоб додати бота в групу/канал, додайте туди бота [@getmyid_bot](https://t.me/getmyid_bot) або перешліть повідомлення з каналу — ви отримаєте ID каналу (починається з `-100...`, наприклад `-1001234567890`).
3. Запишіть ці ID через кому в `ALLOWED_CHATS`.

---

## ⚙️ Покрокова інструкція запуску 24/7 (Безкоштовно)

### Варіант А. Запуск на безкоштовному сервері Oracle Cloud (Рекомендовано 24/7)
Oracle Cloud надає **Always Free VM (Ubuntu)**, на якій бот працюватиме цілодобово без витрат.

1. **Підключіться до вашого VPS через SSH:**
   ```bash
   ssh ubuntu@YOUR_SERVER_IP
   ```

2. **Оновіть пакети та встановіть Python:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3 python3-venv python3-pip git
   ```

3. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/Arpmagic/mops-dyadya-pyos-bot.git mops_bot
   cd mops_bot
   ```

4. **Створіть віртуальне середовище та встановіть залежності:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Налаштуйте файл конфігурації `.env`:**
   ```bash
   cp .env.example .env
   nano .env
   ```
   Вставте ваші токени та ID, натисніть `Ctrl+O` ➔ `Enter` ➔ `Ctrl+X` для збереження.

6. **Налаштуйте автозапуск 24/7 через Systemd:**
   Створіть сервіс:
   ```bash
   sudo nano /etc/systemd/system/mops-bot.service
   ```
   Вставте наступний контент:
   ```ini
   [Unit]
   Description=Mops Dyadya Pyos Telegram Bot 24/7 Service
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/mops_bot
   ExecStart=/home/ubuntu/mops_bot/venv/bin/python main.py
   Restart=always
   RestartSec=5
   Environment=PYTHONUNBUFFERED=1

   [Install]
   WantedBy=multi-user.target
   ```
   Запустіть та увімкніть автозапуск:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable mops-bot.service
   sudo systemctl start mops-bot.service
   ```
   Перевірте статус:
   ```bash
   sudo systemctl status mops-bot.service
   ```

---

### Варіант Б. Запуск через Docker / Docker Compose
1. Встановіть Docker та Docker Compose.
2. Створіть та заповніть `.env`.
3. Запустіть контейнер у фоновому режимі:
   ```bash
   docker compose up -d --build
   ```
4. Перегляд логів:
   ```bash
   docker compose logs -f
   ```

---

### Варіант В. Локальний запуск (Windows / macOS / Linux)
```bash
git clone https://github.com/Arpmagic/mops-dyadya-pyos-bot.git
cd mops-dyadya-pyos-bot
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Заповніть .env своїми ключами
python main.py
```

---

## 💬 Як підключити бота до коментарів каналу

1. **Створіть або відкрийте ваш Telegram-канал.**
2. Перейдіть у **Налаштування каналу** ➔ **Обговорення (Коментарі)** ➔ створіть або прив'яжіть групу (наприклад, *«Обговорення»*).
3. **Додайте вашого бота:**
   * Додайте бота як **адміністратора в канал**.
   * ⚠️ **ВАЖЛИВО:** Додайте бота також **у прив'язану групу «Обговорення»** як адміністратора (щоб він міг читати та писати в коментарях).
4. Тепер будь-яке запитання або челендж у коментарях отримуватиме відповідь **строго в гілці коментарів**!

---

## 🎮 Команди та Тригери

### 📌 Основні команди:
| Команда | Опис |
|---|---|
| `/start` | Привітання та головне меню |
| `/help` | Повна довідка та список челенджів |
| `/role` | Вибір особистості (Мопс, Знаток, Прожарка, Лютий, Братва) |
| `/model` | Вибір або перемикання AI моделі |
| `/reset` | Очистити пам'ять бесіди поточного чату |
| `/los` | Зарядити лося за донат 💥 |
| `/lyash` | Прописати сочного ляща 👋 |
| `/chifir` | Заварити ядрьоний чифір ☕ |
| `/donat` | Збір на м'ясо та грев 💸 |

### 🥊 Текстові тригери стрім-челленджів (працюють прямо в тексті):
* `Лось с разбега` / `Лось з розбігу` / `Королевский лось`
* `Муха`
* `Черепаха`
* `Пылесос` / `Пилосос`
* `Смачный лящ` / `Смачний лящ` / `Лящ`
* `Пробить фанеру`
* `Шокер` / `Травмат`
* `Чифир` / `Чифір`
* `Баба Вася` / `Пес Тузик` / `Хованский`

---

## 📁 Структура проєкту

```text
mops_bot/
├── bot/
│   ├── handlers/          # Обробники повідомлень, команд та адмінки
│   │   ├── admin.py       # Адмін-панель та статистика
│   │   ├── common.py      # Стрім-команди, ролі, моделі
│   │   └── messages.py    # Інтелектуальний роутинг, тригери, коментарі
│   ├── prompts/           # Енциклопедія лору та системні промпти
│   │   └── personas.py    # База знань Мопса і Щадила
│   ├── services/          # Сервіси інтеграцій
│   │   ├── gemini_client.py   # Клієнт Google Gemini API з каскадом
│   │   ├── key_pool.py        # Пул та ротація API ключів
│   │   ├── llm_router.py      # Роутер AI-моделей
│   │   ├── memory.py          # SQLite асинхронна пам'ять діалогів
│   │   └── vault.py           # Офлайн-цитатник на випадок збоїв мережі
│   └── config.py          # Налаштування pydantic-settings
├── data/                  # SQLite база даних розмов (створюється автоматично)
├── .env.example           # Приклад конфігураційного файлу
├── .gitignore             # Захист конфіденційних даних
├── docker-compose.yml     # Скрипт розгортання в Docker
├── Dockerfile             # Збірка Docker-образу
├── main.py                # Головна точка входу бота
├── requirements.txt       # Залежності Python
└── README.md              # Документація проєкту
```

---

## 🍖 Підтримати проєкт (Донат на м'ясо та чифір Мопсу)

Якщо вам сподобався цей бот і ви хочете підтримати автора копійкою на чай/чифір, сосиски та оплату серверів:

### 💳 Швидкі донати:
* 🐱 **Monobank (Банка):** [send.monobank.ua/jar/8HBjkw7ZT5](https://send.monobank.ua/jar/8HBjkw7ZT5)
* 💳 **Номер картки Банки:** `4874 1000 3253 5083`
* ☕ **Buy Me a Coffee:** [buymeacoffee.com/arpmag](https://buymeacoffee.com/arpmag)
* 💸 **Donatello (Віджет стрімера):** [donatello.to/widget/...](https://donatello.to/widget/6a943d6f5649df604b787dd1/token/0b77d459fc1e8838cd9fd6b94fa86c78)

---

### 💎 Криптовалюта (Crypto):
| Мережа / Валюта | Адреса гаманця |
|---|---|
| 🟡 **BNB Smart Chain (BEP20 / BNB / USDT)** | `0x71d9C5f2cF8a8d7cF7a037EF51D1844D2f2C6dDe` |
| 🟣 **Solana (SOL / SPL Tokens)** | `5WjFfpV9zQ4mtTGVceQ1SpDMEAHwX1RwdhTzZDgCiznA` |
| 🔴 **Tron (TRC20 / USDT / TRX)** | `TXot4qHHkVgrWqq44EQb2qsf1DM55ybMDd` |
| 🔷 **Ethereum (ERC20 / ETH / USDT)** | `0x71d9C5f2cF8a8d7cF7a037EF51D1844D2f2C6dDe` |
| 🟠 **Bitcoin (BTC)** | `bc1qjlrlelxw3tt80xnsq8xgtazas6tlzre2txav42` |

<details>
<summary>📱 <b>Натисніть тут, щоб переглянути QR-коди для сканування</b></summary>
<br>

<p align="center">
  <b>Buy Me a Coffee</b><br>
  <img src="assets/qr/buymeacoffee.png" width="220" alt="Buy Me a Coffee QR" /><br><br>
  <b>BNB Smart Chain</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Solana (SOL)</b><br>
  <img src="assets/qr/bnb.jpg" width="200" alt="BNB QR" /> &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/qr/solana.jpg" width="200" alt="Solana QR" /><br><br>
  <b>Tron (TRC20 USDT)</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Ethereum (ETH)</b><br>
  <img src="assets/qr/tron.png" width="200" alt="Tron QR" /> &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/qr/ethereum.jpg" width="200" alt="Ethereum QR" />
</p>
</details>

---

## ⚖️ Ліцензія та Подяка

Проєкт створено в освітніх та розважальних цілях для фанатів класичного YouTube-фольклору.  
Поширюється за ліцензією [MIT](LICENSE).

**От душы душевно в душу, головы родные! Гав-гав! 🐶🍖**
