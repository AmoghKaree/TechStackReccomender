# Tech Stack Recommendation Report

## Project Overview

The user wants to build a SaaS dashboard for tracking fitness metrics, including workout logging, progress charts, and social features like leaderboards. This is a small-scale web application built by a solo developer on a free-tier budget, targeting a few hundred users initially with plans to grow over time.

## Recommended Stack

### Frontend
**Recommendation: React** (Score: 8.8/10)
- Why: React offers the largest ecosystem of charting and UI component libraries, which is critical for a metrics dashboard. The extensive community means nearly every problem a solo developer encounters has already been solved and documented. Its component-based architecture makes it straightforward to build reusable chart widgets and dashboard panels.
- Runner-up: Vue.js (Score: 8.4/10) — Vue offers an easier learning curve and excellent documentation, but its smaller charting ecosystem means more custom work for specialized dashboard visualizations.

### Backend
**Recommendation: FastAPI** (Score: 8.7/10)
- Why: FastAPI provides automatic API documentation via Swagger UI, which accelerates solo development by eliminating the need to manually document endpoints. Its async support handles concurrent dashboard data requests efficiently, and Python's data science ecosystem integrates naturally for any server-side metric calculations. The learning curve is gentle for developers already familiar with Python.
- Runner-up: Express.js (Score: 8.4/10) — Express is more flexible but requires more boilerplate for validation, documentation, and error handling that FastAPI provides out of the box.

### Database
**Recommendation: Supabase (PostgreSQL)** (Score: 8.7/10)
- Why: Supabase provides a hosted PostgreSQL database with a generous free tier (500MB storage, unlimited API requests), which fits the budget constraint perfectly. It includes a built-in REST API and real-time subscriptions, reducing the amount of backend code needed. PostgreSQL's native JSON support and window functions are well-suited for time-series fitness data and leaderboard queries.
- Runner-up: PlanetScale (Score: 7.4/10) — PlanetScale offers excellent scalability but its MySQL foundation lacks PostgreSQL's native JSON operators and window functions that simplify analytics queries.

### Hosting
**Recommendation: Vercel** (Score: 8.7/10)
- Why: Vercel's free tier includes automatic HTTPS, global CDN, and seamless Git-based deployments, which eliminates DevOps overhead for a solo developer. The platform handles frontend hosting natively and supports serverless API routes as a fallback. Preview deployments for every pull request streamline the development workflow even for a single developer iterating quickly.
- Runner-up: Railway (Score: 7.5/10) — Railway offers more flexibility for backend deployment but its free tier is more limited (500 hours/month) and requires more configuration than Vercel's zero-config approach.

### Authentication
**Recommendation: Supabase Auth** (Score: 8.7/10)
- Why: Since Supabase is already recommended for the database, using Supabase Auth eliminates an entire integration layer. It provides email/password, OAuth (Google, GitHub, Apple), and magic link authentication out of the box with row-level security policies that tie directly into the database. This is the most cost-effective and architecturally clean option for this specific stack.
- Runner-up: Clerk (Score: 7.9/10) — Clerk offers a more polished pre-built UI for login flows, but adds a separate service dependency and its free tier caps at 10,000 monthly active users, which is sufficient but introduces an unnecessary external dependency.

## Stack Synergy

This stack is intentionally built around Supabase as the central platform. By using Supabase for both the database and authentication, the system eliminates two integration boundaries that would otherwise require custom glue code. React's ecosystem includes first-class Supabase client libraries (@supabase/supabase-js) that handle real-time subscriptions and auth state management with minimal setup. FastAPI serves as a lightweight processing layer for any logic too complex for direct database queries, such as aggregating weekly progress reports or computing personal records. Vercel's deployment model pairs naturally with React and can proxy API requests to a separately hosted FastAPI service on Railway's free tier if serverless functions prove insufficient.

## Tradeoffs & Risks

- **Supabase vendor concentration**: Using Supabase for both database and auth creates a single point of dependency. If Supabase changes its pricing or experiences downtime, multiple layers are affected. Mitigation: Supabase is open-source and self-hostable as a fallback.
- **FastAPI hosting on Vercel limitations**: Vercel's serverless functions have a 10-second execution timeout on the free tier, which may be insufficient for complex data aggregation queries. If this becomes a bottleneck, the FastAPI backend should be migrated to Railway or Render.
- **React bundle size**: For a metrics dashboard with multiple charting libraries (Recharts, Chart.js), the initial JavaScript bundle may become large. Code splitting and lazy loading should be implemented early to maintain acceptable load times.
- **Free tier scaling ceiling**: The combined free tiers support approximately 500 monthly active users comfortably. Beyond that threshold, costs will begin to accumulate across Supabase ($25/month Pro plan) and hosting. This should be planned for before reaching capacity.

## Areas of Uncertainty

All five stack categories scored above the 7.0 confidence threshold on the first evaluation pass. No categories required re-research, indicating strong alignment between the stated requirements and the recommended technologies.

## Evaluation Metadata
- Iterations completed: 0
- Confidence threshold: 7.0/10
- Categories that required re-research: none

---
*Generated by Tech Stack Recommender — an agentic AI system*