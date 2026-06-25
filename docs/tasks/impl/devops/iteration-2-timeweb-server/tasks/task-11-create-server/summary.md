# Task 11 summary

## Сделано

- SSH keys сгенерированы локально (`~/.ssh/diaai-admin`, `~/.ssh/diaai-deploy`) и загружены в Timeweb (IDs 708193, 708195)
- VPS создан после OK пользователя

## Сервер

| Поле | Значение |
|------|----------|
| ID | `8460897` |
| Name | `diaai-prod` |
| Region | `ru-3` (msk-1) — `ru-1`/`ru-2` вернули `no_free_node` |
| Preset | `4801` (2 vCPU, 4 GB, 50 GB NVMe) — аналог 2453 в ru-3 |
| OS | Ubuntu 24.04 |
| IPv4 | `201.51.4.34` |
| IPv6 | `2a03:6f00:a::2:ac5f` |
| SSH user | `root` |
| SSH key | `diaai-admin` (default) |

## Verify

```bash
ssh -i ~/.ssh/diaai-admin root@201.51.4.34 'uname -a'
# Linux ... Ubuntu 24.04.4 LTS ✅
```

## Отклонения

- Регион **ru-3** вместо ru-1 из-за отсутствия свободных нод в ru-1/ru-2
- Preset **4801** вместо 2453 (тот же класс конфигурации в ru-3)
- Ключи сгенерированы агентом (task 10 пользовательская часть не была выполнена)

## Отложено

- Inventory template — task 12
