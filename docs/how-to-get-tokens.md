# Как получить токены для diaai

Краткая инструкция: Telegram Bot Token и OpenRouter API key.  
Реальные ключи в репозиторий не коммитить — только в локальный `.env`.

---

## 1. Telegram Bot Token (BotFather)

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather).
2. Отправьте команду `/start`.
3. Создайте нового бота: `/newbot`.
4. Введите **display name** (как бот будет называться в чатах).
5. Введите **username** — должен заканчиваться на `bot` (например, `my_diaai_helper_bot`).
6. BotFather пришлёт сообщение с токеном вида `123456789:ABCdef...`.
7. Скопируйте токен в `.env`:

   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_сюда
   ```

**Полезные команды BotFather**

| Команда | Назначение |
|---------|------------|
| `/mybots` | список ваших ботов, настройки |
| `/token` | перевыпустить токен (старый перестанет работать) |
| `/setdescription` | описание бота |
| `/setcommands` | меню команд |

**Официальная документация**

- [Telegram Bots: An introduction for developers](https://core.telegram.org/bots)
- [BotFather](https://core.telegram.org/bots#6-botfather)

---

## 2. OpenRouter API key

1. Откройте [openrouter.ai](https://openrouter.ai/) и зарегистрируйтесь (Google, GitHub или email).
2. Перейдите в раздел ключей: [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys).
3. Нажмите **Create Key** (или аналогичную кнопку создания ключа).
4. Задайте имя ключа (например, `diaai-local`) и сохраните.
5. Скопируйте ключ **сразу** — повторно его могут не показать.
6. Добавьте в `.env`:

   ```env
   OPENROUTER_API_KEY=ваш_ключ_сюда
   LLM_MODEL=openrouter/auto
   ```

   `LLM_MODEL` — идентификатор модели на OpenRouter. Для фото нужна vision-модель; список: [openrouter.ai/models](https://openrouter.ai/models).

**Баланс и лимиты**

- Пополнение и usage: [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits)
- Документация API: [openrouter.ai/docs](https://openrouter.ai/docs)

---

## 3. Проверка

1. Скопируйте `.env.example` → `.env` и заполните переменные.
2. Запустите:

   ```bash
   make install && make run
   ```

3. Найдите бота в Telegram по username и отправьте `/start`.

Если бот не отвечает — проверьте токен Telegram, ключ OpenRouter и что `LLM_MODEL` указан корректно.
