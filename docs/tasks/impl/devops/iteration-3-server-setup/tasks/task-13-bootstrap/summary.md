# Task 13 summary

## Сделано

- [`devops/server/bootstrap.sh`](../../../../../../devops/server/bootstrap.sh) — Docker 29.6, compose v5.2, git/curl/make, ufw, user `deploy`, `/opt/diaai`
- Прогон на production VPS `201.51.4.34`

## Verify (2025-06-25)

```text
docker compose version → v5.2.0 ✅
ufw: 22, 3000, 8000 ✅
deploy user: groups deploy docker ✅
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 'docker compose version' ✅
/opt/diaai owned by deploy ✅
```

## Команда повторного прогона

```bash
scp devops/server/bootstrap.sh ~/.ssh/diaai-deploy.pub root@201.51.4.34:/tmp/
ssh root@201.51.4.34 'bash /tmp/bootstrap.sh'
```

## Отложено

- Layout repo + `.env` — task 14
- Stack на VPS — task 15
