# Task 18 summary

## E2E

| Run | Commit | Result |
|-----|--------|--------|
| 1 | `120710e` | Deploy SSH OK; `stack-health` FAIL — web cold start |
| 2 | fix wait loop | → после push |

## Verify (после run 1, stack уже live)

```text
curl http://201.51.4.34:8000/health → ok
curl http://201.51.4.34:3000/ → 307
POST login ivan_p → 200 (task 15)
```

## Pipeline

push main → Docker Publish ✅ → Deploy (workflow_run) → git pull + stack registry

## Fix

`deploy.yml`: retry curl :3000 до 90s перед `make stack-health`

## Docs

tasklist iter 4 ✅ · plan · architecture · onboarding · smoke-test
