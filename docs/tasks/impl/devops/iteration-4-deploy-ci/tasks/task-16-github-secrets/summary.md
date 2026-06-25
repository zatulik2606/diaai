# Task 16 summary

## Сделано

- [`devops/deploy/github-secrets.md`](../../../../../../devops/deploy/github-secrets.md)
- Secrets через `gh secret set`: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`

## Verify

```bash
ssh -i ~/.ssh/diaai-deploy deploy@201.51.4.34 → OK (task 13)
gh secret list → 3 secrets
```
