# Project 20: Capstone — Integrated Multi-Tier Azure Platform

## What this project demonstrates
A genuinely integrated system, not standalone demos: a serverless API tier (Azure Functions) connecting to a real Azure SQL Database, with monitoring, CI/CD automation, and cost governance wrapped around it — bringing together skills from all 19 prior projects into one working whole.

## Architecture
```
GitHub (main branch)
-> GitHub Actions (CI/CD)
-> Azure Function App (learn-capstone-api)
-> Application Insights (auto-attached monitoring)
-> Azure SQL Database (capstone-db)
-> Firewall rule: AllowAzureServices

Cost Governance: Monthly budget alert on learn-cloud-capstone-rg
```

## What I learned
- **True multi-tier integration**: an API tier and a Data tier, genuinely connected and verified end-to-end, not just deployed side by side
- **Connection strings and app settings**: securely storing database credentials as Function App settings, rather than hardcoded or committed to source control
- **Firewall rules for Azure-to-Azure communication**: the special `0.0.0.0`-`0.0.0.0` rule that specifically allows other Azure services (not the public internet) to reach a SQL Server
- **A genuine, real debugging investigation**: GitHub Actions' zip-deploy method for Azure Functions on the Linux Consumption plan did not reliably trigger a remote build step, meaning `pyodbc` (which requires native compilation) failed to install correctly through that specific deployment path — even though the exact same code deployed and worked perfectly via `func azure functionapp publish`, which does trigger a proper remote build automatically
- Diagnosed this by systematically ruling out causes: confirmed the function was registered, confirmed app settings were correctly set, confirmed the Function host itself was healthy (via the `/admin/host/status` endpoint returning 401, not 404), which isolated the problem specifically to the custom function's dependency loading — not authentication, not configuration, not the platform itself
- Explored switching to a pure-Python SQL driver (`python-tds`) to avoid the native-dependency problem entirely, and hit a second, genuine issue: `python-tds`'s TLS code is incompatible with current `pyOpenSSL` versions (a real, documented open-source library compatibility gap) — made the pragmatic engineering call to revert to the proven, working `pyodbc` + manual deployment approach rather than chase an unbounded dependency rabbit hole
- This mirrors a real, honest platform limitation of Azure Functions' Linux Consumption plan with native-dependency Python packages — documented here rather than hidden, consistent with this entire project series' approach to debugging

## Tools used
- Azure Functions (Python, Consumption plan)
- Azure SQL Database
- Application Insights (auto-attached)
- GitHub Actions (CI/CD, with a documented known limitation)
- Azure Cost Management (budget alert)
- Azure CLI, Azure Functions Core Tools

## Proof it works

**Live API successfully querying the database, deployed and verified end-to-end:**
![API and DB connected](screenshots/project20-api-db-connected.png)

## Honest debugging notes
GitHub Actions' zip-deploy to Azure Functions Linux Consumption did not reliably build native-dependency packages (`pyodbc`), producing a silent 404 on all routes despite successful-looking deployment logs. Diagnosed via systematic elimination (function registration, app settings, host health) rather than guesswork. Resolved by using the Azure Functions Core Tools' `publish` command, which triggers a genuine remote build. This is a known constraint of the platform, and in a production setting would likely be addressed by migrating to Azure's newer Flex Consumption plan or a container-based deployment, both of which handle native dependencies more reliably.

## Cost note
Function App (Consumption), SQL Database (Basic tier), and Application Insights are all low-cost. A €10/month budget alert is configured on the resource group. Resources torn down after project completion.
