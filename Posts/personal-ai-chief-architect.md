# Personal AI Chief & Architect

Personal AI Chief & Architect — пакет для мультиагента, который совмещает навыки секретаря и инженера-архитектора.

## Что внутри

- Telegram как единый канал общения.
- Gmail и Google Calendar для входящих, встреч, briefings и follow-up.
- Google Drive для документов и ADR.
- GitHub для issues, архитектурных решений, веток и draft PR.
- Skills `orchestrator`, `secretary`, `architect`, `integrations`, `adr`, `privacy`.
- Hooks на сообщения, встречи, документы, задачи и pull request.
- Loops: morning briefing, inbox triage, architecture review, follow-up.
- Confirmation gates и least-privilege policy для всех внешних записей.

## Важное ограничение

Пакет не содержит токенов и не выполняет сетевые вызовы до настройки проверенных MCP-адаптеров. Это позволяет сначала проверить маршрутизацию, права и preview действий, а затем включать интеграции по одной.

Исходники: `plugins/personal-ai-chief-architect/`.
