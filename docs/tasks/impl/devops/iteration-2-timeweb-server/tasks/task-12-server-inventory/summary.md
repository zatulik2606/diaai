# Task 12 summary

## Сделано

- [`devops/server/inventory.example.md`](../../../../../../devops/server/inventory.example.md) — шаблон + production values в таблице
- SSH verify: `root@201.51.4.34` по `diaai-admin` ✅
- Deploy key добавлен на сервер: `twc ssh-key add 8460897 708195`
- Обновлены `architecture.md`, `plan.md`, `devops/server/README.md`, `twc-cli.md`

## Verify

```text
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'uname -a' → Ubuntu 24.04.4 LTS ✅
```

## Отклонения

- Inventory example содержит реальный IP/server id (не секрет; private keys не в git)
