# Runbook активации интеграций

Этот документ описывает безопасное включение Telegram, Gmail, Google Calendar, Google Drive и GitHub для `personal-ai-chief-architect`.

## Текущее состояние

По умолчанию пакет не подключён к внешним сервисам. `scripts/mcp_adapter.py` — намеренная заглушка: она возвращает `not_configured` и не делает сетевых вызовов. Одного заполнения переменных окружения недостаточно — нужно заменить заглушку на проверенный MCP-сервер или адаптер и сохранить его команду в `.mcp.json`.

Активация выполняется по схеме:

1. credentials и минимальные права;
2. read-only smoke test;
3. проверка маршрутизации и журналирования;
4. отдельное включение каждой записи с confirmation gate.

## 1. Подготовить секреты

Используйте локальный secret manager или файл на машине, который не попадает в Git. Шаблон переменных находится в [`.env.example`](../.env.example):

```text
TELEGRAM_BOT_TOKEN=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REFRESH_TOKEN=
GITHUB_TOKEN=
```

Правила:

- в dotenv-файле должны быть только строки `KEY=VALUE` и комментарии;
- не вставляйте токены в команды, сообщения, логи, issue или commit;
- не выводите `.env` через `cat`, `printenv` или `set`;
- задайте права файла `chmod 600 path/to/.env`, если используете файл;
- после случайной публикации немедленно отзовите токен и создайте новый.

Адаптер должен получать эти значения через окружение или secret manager. Не добавляйте реальные credentials в `.mcp.json`.

## 2. Создать reviewed MCP-адаптер

В `.mcp.json` сохранены логические серверы `telegram`, `google-workspace` и `github`. Для активации замените только `command` и `args` заглушки на команды проверенных адаптеров:

```json
{
  "command": "path/to/reviewed-adapter",
  "args": ["telegram"],
  "env": {"TELEGRAM_BOT_TOKEN": "${TELEGRAM_BOT_TOKEN}"}
}
```

Пример показывает форму конфигурации, а не готовый путь. Адаптер должен:

- валидировать входные параметры и таймзону;
- разделять read и write операции;
- возвращать структурированный preview до записи;
- не писать токены в ответы и логи;
- иметь timeout, retry policy и понятные ошибки 401/403/429;
- оставлять внешнюю запись заблокированной, пока оркестратор не получил подтверждение.

Не включайте все сервисы одним изменением: сначала проверьте один адаптер и один read-only вызов.

## 3. Telegram

1. В Telegram откройте `@BotFather`, выполните `/newbot` и сохраните выданный bot token в `TELEGRAM_BOT_TOKEN`.
2. Настройте username и privacy mode бота под нужный чат. Для личного диалога пользователь должен первым открыть чат и отправить сообщение.
3. Запретите отправку сообщений на первом этапе: разрешите только receive и draft.
4. Проверка адаптера: отправьте боту тестовое сообщение и убедитесь, что оно попало в локальный входящий поток, но не вызвало автоматический ответ.
5. После подтверждения включите `telegram.send` и проверьте preview: получатель, текст и время отправки.

Токен Telegram обладает полным контролем над ботом, поэтому храните его как пароль и отзывайте через BotFather при утечке. См. [официальное руководство Telegram Bots](https://core.telegram.org/bots) и [tutorial](https://core.telegram.org/bots/tutorial).

## 4. Gmail, Google Calendar и Google Drive

Для одного пользователя используйте OAuth client ID и offline access. Для нескольких пользователей Google Workspace используйте отдельную схему с service account/domain-wide delegation только при необходимости и с согласованием администратора. Google описывает выбор credentials в [Create access credentials](https://developers.google.com/workspace/guides/create-credentials) и server-side refresh token flow в [Gmail authorization](https://developers.google.com/workspace/gmail/api/auth/web-server).

1. Создайте или выберите Google Cloud project.
2. Включите Gmail API, Google Calendar API и Google Drive API.
3. Настройте OAuth consent screen и OAuth client ID подходящего типа.
4. Выполните авторизацию с `access_type=offline`, получите refresh token и сохраните его только как `GOOGLE_REFRESH_TOKEN`.
5. Сначала запросите только read-only scopes:

   | Сервис | Начальный scope | Запись включать позже |
   |---|---|---|
   | Gmail | `https://www.googleapis.com/auth/gmail.readonly` | `gmail.send` для отправки; `gmail.modify` для archive/labels |
   | Calendar | `https://www.googleapis.com/auth/calendar.events.readonly` или более узкий scope | `https://www.googleapis.com/auth/calendar.events` для create/update |
   | Drive | `https://www.googleapis.com/auth/drive.file` для выбранных/созданных приложением файлов | расширять только при доказанной необходимости |

   Для Drive предпочитайте `drive.file`: Google указывает его как более узкий per-file доступ. Полный `drive` scope не включайте по умолчанию. См. [Drive scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth), [Gmail scopes](https://developers.google.com/workspace/gmail/api/auth/scopes) и [Calendar authorization](https://developers.google.com/workspace/calendar/api/auth).

6. Запустите read-only smoke tests:

   - Gmail: прочитать количество unread и заголовки одного thread, не загружая лишнее содержимое;
   - Calendar: прочитать ближайшее событие и проверить таймзону;
   - Drive: перечислить только разрешённые файлы или проверить один заранее выбранный файл.

7. Включайте записи по одной:

   - Gmail: сначала draft, затем отправка только после preview и подтверждения;
   - Calendar: create/update с точным временем, таймзоной, участниками и текстом приглашения в preview;
   - Drive: запись только в заранее известный файл или каталог, без удаления.

8. После смены scopes повторите OAuth consent flow и обновите refresh token. Не добавляйте новый scope молча: это изменение уровня доступа.

## 5. GitHub

Для `AABrovarnik/NewAge` создайте fine-grained personal access token, ограниченный только этим репозиторием. Начальная конфигурация:

| Permission | Read-only rollout | После отдельного подтверждения |
|---|---:|---:|
| Metadata | Read | Read |
| Contents | Read | Read and write для branch/push |
| Issues | Read | Read and write для issue/comment |
| Pull requests | Read | Read and write для PR/review |
| Workflows | Не выдавать | Только если требуется изменение workflow-файлов |

Сначала проверьте чтение repository metadata, issues и pull requests. Для push нужен Contents write; право на Workflows не добавляйте без отдельной потребности. Таблицу endpoint-to-permission поддерживает [GitHub permissions reference](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens).

После проверки read-only включите операции в такой последовательности:

1. создать ветку;
2. подготовить diff и draft PR;
3. показать пользователю target, scope и diff;
4. выполнить push только после подтверждения;
5. submit/merge оставить отдельными действиями с отдельным подтверждением.

Токен передавайте адаптеру через `GITHUB_TOKEN`. Не встраивайте его в remote URL, shell history или сообщения.

## 6. Проверка пакета и dry-run

Из корня репозитория выполните:

```bash
python3 plugins/personal-ai-chief-architect/scripts/preflight.py
python3 plugins/personal-ai-chief-architect/scripts/run_loop.py morning-briefing --dry-run
python3 plugins/personal-ai-chief-architect/scripts/run_loop.py inbox-triage --dry-run
python3 /root/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/personal-ai-chief-architect
```

Ожидаемый результат: `preflight: OK`, планы loops без внешней записи и успешная валидация плагина. `run_loop.py` печатает план; он не заменяет smoke test реального адаптера.

## 7. Критерии готовности

Интеграция считается активированной только если:

- read-only вызов прошёл с ожидаемым аккаунтом;
- scope/permission не шире необходимого;
- preview показывает target, scope и diff;
- write-вызов заблокирован без явного подтверждения;
- ошибки и audit event не содержат credentials;
- есть процедура revoke/rotate и понятный владелец интеграции.

При 401 остановитесь и обновите credentials. При 403 сначала проверьте scope, repository access и организационные approval requirements. При 429 не увеличивайте права — настройте backoff и ограничение частоты.
