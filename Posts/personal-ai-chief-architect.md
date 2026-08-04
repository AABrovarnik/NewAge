# Personal AI Chief & Architect

Personal AI Chief & Architect — локальный Codex-плагин для мультиагента, который совмещает роль секретаря и инженера-архитектора. Пакет помогает собрать контекст, подготовить решение и передать внешнее действие на подтверждение пользователя.

## Что входит в пакет

- Канал Telegram для входящих сообщений и черновиков ответов.
- Gmail и Google Calendar для triage входящих, встреч, briefings и follow-up.
- Google Drive для документов и ADR.
- GitHub как инженерный источник: issues, контекст репозитория, ветки и draft PR.
- Skills `orchestrator`, `secretary`, `architect`, `integrations`, `adr`, `privacy`.
- Hooks на сообщения, события календаря, документы, задачи и pull request.
- Loops `morning-briefing`, `inbox-triage`, `architecture-review` и `follow-up`.
- Политика least privilege с confirmation gates для внешних записей.

Основной исходный код находится в [`plugins/personal-ai-chief-architect/`](../plugins/personal-ai-chief-architect/). Точки входа и правила описаны в [README](../plugins/personal-ai-chief-architect/README.md), [конфигурации интеграций](../plugins/personal-ai-chief-architect/docs/integrations.md), [hooks](../plugins/personal-ai-chief-architect/hooks/hooks.json), [loops](../plugins/personal-ai-chief-architect/loops/) и [политике разрешений](../plugins/personal-ai-chief-architect/policies/permissions.yaml).

## Модель безопасности

- Чтение используется по умолчанию для почты, календаря, Drive и GitHub.
- Отправка, публикация, изменение встреч, push, submit PR, merge и запись в Drive требуют явного подтверждения.
- Удаление репозитория и force-push запрещены политикой.
- Токены и OAuth refresh tokens не должны попадать в сообщения, логи или коммиты; `.env` исключён из Git.

## Важное ограничение

Пакет содержит integration points, но не является готовым credential broker. Включённый `mcp_adapter.py` намеренно не выполняет сетевые вызовы и возвращает статус `not_configured`. Перед production-использованием нужно подключить проверенные MCP-серверы или адаптеры, настроить переменные окружения и проверить права каждой интеграции отдельно.

Такой режим позволяет сначала проверить маршрутизацию, разрешения и preview действий, а затем безопасно включать внешние записи по одной.

## Проверка

Локальные проверки выполняются без сетевых вызовов:

```bash
python3 plugins/personal-ai-chief-architect/scripts/preflight.py
python3 /root/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/personal-ai-chief-architect
```

Обе проверки пройдены для текущей версии пакета.
