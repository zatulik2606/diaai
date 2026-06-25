# Task 12 summary

## Сделано

- [`devops/server/inventory.example.md`](../../../../../../devops/server/inventory.example.md) — IP, OS, server id, SSH
- [`devops/server/README.md`](../../../../../../devops/server/README.md) § Проверка SSH
- [`docs/devops/twc-cli.md`](../../../../../../docs/devops/twc-cli.md) §3 Проверка SSH
- SSH verify: admin + deploy ✅
- Обновлены architecture, plan, tasklist

## Verify

```text
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'uname -a' → Ubuntu 24.04.4 LTS ✅
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'whoami' → deploy ✅
```
