MOCK_CLARIFIER_RESPONSE = {
    "project_summary": "A SaaS web dashboard for tracking fitness metrics including workout logging, progress visualization, and social features like leaderboards and activity sharing.",
    "project_type": "web_app",
    "scale": "small",
    "team_size": "solo",
    "budget": "free_tier",
    "performance_requirements": "moderate",
    "tech_familiarity": {
        "frontend": "intermediate",
        "backend": "intermediate",
        "databases": "beginner",
        "devops": "beginner"
    },
    "key_features": [
        "User authentication and profiles",
        "Workout logging with custom exercises",
        "Progress charts and visualizations",
        "Social feed and leaderboards",
        "Mobile-responsive design"
    ],
    "constraints": [
        "Must stay within free-tier pricing",
        "Solo developer — minimal DevOps overhead preferred",
        "Needs to support a few hundred users initially"
    ],
    "assumptions": [
        "Team familiarity with frontend assumed intermediate based on mention of dashboard UI",
        "Backend familiarity assumed intermediate based on SaaS scope",
        "Database and DevOps familiarity assumed beginner since not mentioned",
        "Performance requirements assumed moderate — dashboards need fast chart rendering but not real-time sub-millisecond latency",
        "No mobile app required — responsive web is sufficient"
    ]
}

MOCK_RESEARCHER_RESPONSE = {
    "frontend": [
        {
            "name": "React",
            "description": "A component-based JavaScript library for building user interfaces, maintained by Meta with the largest ecosystem of third-party libraries.",
            "pros": [
                "Massive ecosystem of charting libraries (Recharts, Chart.js, Nivo) ideal for fitness dashboards",
                "Huge community means nearly every problem has an existing solution on Stack Overflow",
                "Component reusability makes it easy to build consistent dashboard panels"
            ],
            "cons": [
                "Steeper initial learning curve compared to simpler frameworks",
                "Requires additional libraries for state management and routing that add complexity"
            ]
        },
        {
            "name": "Svelte",
            "description": "A compiler-based frontend framework that shifts work from runtime to build time, producing highly optimized vanilla JavaScript.",
            "pros": [
                "Simpler syntax with less boilerplate — faster development for a solo developer",
                "Smaller bundle sizes mean faster load times for dashboard pages",
                "Built-in reactivity without needing external state management"
            ],
            "cons": [
                "Smaller ecosystem — fewer pre-built charting components available",
                "Fewer job market resources and tutorials compared to React"
            ]
        },
        {
            "name": "Vue.js",
            "description": "A progressive JavaScript framework known for its gentle learning curve and excellent documentation.",
            "pros": [
                "Easiest learning curve among the three — good for a solo developer managing everything",
                "Strong documentation and official libraries for routing and state management",
                "Good charting support through libraries like vue-chartjs and ECharts"
            ],
            "cons": [
                "Smaller ecosystem than React in the English-speaking community",
                "Fewer third-party component libraries for specialized dashboard widgets"
            ]
        }
    ],
    "backend": [
        {
            "name": "FastAPI",
            "description": "A modern Python web framework built on Starlette and Pydantic, designed for building APIs with automatic documentation.",
            "pros": [
                "Auto-generated Swagger docs eliminate manual API documentation for a solo developer",
                "Python ecosystem integrates naturally for any server-side data processing or analytics",
                "Async support handles concurrent dashboard requests efficiently"
            ],
            "cons": [
                "Python is slower than Node.js for raw throughput, though not a concern at this scale",
                "Deployment requires a separate server process unlike serverless alternatives"
            ]
        },
        {
            "name": "Express.js",
            "description": "A minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.",
            "pros": [
                "Same language (JavaScript) as the frontend reduces context switching",
                "Massive middleware ecosystem for authentication, logging, and validation",
                "Lightweight and fast with minimal overhead"
            ],
            "cons": [
                "Requires more boilerplate for validation and documentation compared to FastAPI",
                "Callback-based patterns can lead to messy code without discipline"
            ]
        },
        {
            "name": "Django",
            "description": "A batteries-included Python web framework with built-in ORM, admin panel, and authentication system.",
            "pros": [
                "Built-in admin panel provides a free back-office dashboard for managing data",
                "ORM simplifies database interactions for a developer with beginner database skills",
                "Built-in auth system eliminates the need for a separate auth provider"
            ],
            "cons": [
                "Heavier framework — more opinionated and slower to prototype quick API endpoints",
                "Monolithic architecture can feel excessive for a small API-focused project"
            ]
        }
    ],
    "database": [
        {
            "name": "Supabase (PostgreSQL)",
            "description": "An open-source Firebase alternative built on PostgreSQL, offering a hosted database with REST API, real-time subscriptions, and authentication.",
            "pros": [
                "Generous free tier with 500MB storage and unlimited API requests",
                "Built-in REST API reduces backend code needed for CRUD operations",
                "PostgreSQL's window functions and JSON support are ideal for time-series fitness data"
            ],
            "cons": [
                "Vendor dependency — though Supabase is open-source and self-hostable as a fallback",
                "Free tier has limited compute for complex aggregation queries"
            ]
        },
        {
            "name": "PlanetScale",
            "description": "A serverless MySQL-compatible database platform built on Vitess with branching workflows for schema changes.",
            "pros": [
                "Serverless scaling handles traffic spikes without manual configuration",
                "Database branching makes schema changes safer for a solo developer",
                "Strong performance for read-heavy dashboard workloads"
            ],
            "cons": [
                "MySQL lacks PostgreSQL's native JSON operators and window functions useful for analytics",
                "Free tier is more limited than Supabase at 5GB storage but with row read limits"
            ]
        },
        {
            "name": "Firebase Firestore",
            "description": "A NoSQL document database by Google with real-time sync and offline support built in.",
            "pros": [
                "Real-time sync is useful for social features like live leaderboards",
                "Generous free tier with 1GB storage and 50K reads per day",
                "SDKs available for web and mobile with minimal backend code needed"
            ],
            "cons": [
                "NoSQL structure makes complex queries like time-range aggregations difficult",
                "Costs can spike unpredictably with high read volumes on dashboard pages"
            ]
        }
    ],
    "hosting": [
        {
            "name": "Vercel",
            "description": "A cloud platform optimized for frontend frameworks with automatic deployments, global CDN, and serverless functions.",
            "pros": [
                "Zero-config deployments from Git with automatic HTTPS and CDN",
                "Preview deployments for every branch streamline solo development workflow",
                "Generous free tier with 100GB bandwidth per month"
            ],
            "cons": [
                "Serverless functions have a 10-second timeout on free tier limiting complex API routes",
                "Primarily optimized for frontend — backend hosting requires a separate service"
            ]
        },
        {
            "name": "Railway",
            "description": "A cloud platform for deploying full-stack applications with support for databases, backend services, and scheduled tasks.",
            "pros": [
                "Supports both frontend and backend deployment in a single platform",
                "Built-in PostgreSQL hosting if not using Supabase",
                "Simple deployment with automatic builds from GitHub"
            ],
            "cons": [
                "Free tier limited to 500 hours per month which may not cover always-on services",
                "Less CDN optimization for frontend compared to Vercel"
            ]
        },
        {
            "name": "Fly.io",
            "description": "A platform for running full-stack applications close to users with edge computing capabilities.",
            "pros": [
                "Edge deployment means low latency for users regardless of location",
                "Supports persistent processes unlike pure serverless platforms",
                "Free tier includes 3 shared VMs and 160GB outbound transfer"
            ],
            "cons": [
                "More complex setup — requires Docker knowledge that a beginner DevOps developer may lack",
                "Debugging deployed applications is harder than on simpler platforms"
            ]
        }
    ],
    "auth": [
        {
            "name": "Supabase Auth",
            "description": "Built-in authentication service within the Supabase platform supporting email, OAuth, and magic links with row-level security.",
            "pros": [
                "Zero additional cost if already using Supabase for database",
                "Row-level security ties auth directly to database access policies",
                "Supports Google, GitHub, Apple OAuth plus email/password and magic links"
            ],
            "cons": [
                "Tightly coupled to Supabase — switching databases means switching auth too",
                "Less customizable login UI compared to dedicated auth providers"
            ]
        },
        {
            "name": "Clerk",
            "description": "A developer-focused authentication platform with pre-built UI components and session management.",
            "pros": [
                "Beautiful pre-built login and signup components save development time",
                "Excellent React integration with hooks for session management",
                "Free tier supports up to 10,000 monthly active users"
            ],
            "cons": [
                "Adds an external service dependency to the stack",
                "Advanced customization requires upgrading to paid plans"
            ]
        },
        {
            "name": "Auth0",
            "description": "An enterprise-grade identity platform by Okta with extensive provider support and compliance features.",
            "pros": [
                "Supports the widest range of identity providers and enterprise SSO",
                "Extensive documentation and SDKs for every major framework",
                "Built-in compliance features for data protection regulations"
            ],
            "cons": [
                "Free tier limited to 7,500 active users with branding restrictions",
                "Overkill for a small fitness dashboard — complexity not justified at this scale"
            ]
        }
    ]
}

MOCK_EVALUATOR_RESPONSE = {
    "frontend": [
        {
            "name": "React",
            "requirements_fit": 8.5,
            "learning_curve": 7.0,
            "scalability": 9.0,
            "cost": 10.0,
            "community_support": 9.5,
            "average": 8.8,
            "justification": "React's massive charting ecosystem directly addresses the dashboard visualization needs. Learning curve is moderate for an intermediate frontend developer but the wealth of tutorials and community support compensates."
        },
        {
            "name": "Svelte",
            "requirements_fit": 7.5,
            "learning_curve": 8.5,
            "scalability": 7.5,
            "cost": 10.0,
            "community_support": 6.5,
            "average": 8.0,
            "justification": "Svelte's simplicity benefits a solo developer but the smaller ecosystem means more custom work for charting components. Community support is growing but still behind React for niche problems."
        },
        {
            "name": "Vue.js",
            "requirements_fit": 7.5,
            "learning_curve": 9.0,
            "scalability": 8.0,
            "cost": 10.0,
            "community_support": 7.5,
            "average": 8.4,
            "justification": "Vue's gentle learning curve and good documentation make it efficient for a solo developer. Charting support is solid through vue-chartjs though the ecosystem is slightly smaller than React's."
        }
    ],
    "backend": [
        {
            "name": "FastAPI",
            "requirements_fit": 9.0,
            "learning_curve": 8.0,
            "scalability": 8.5,
            "cost": 10.0,
            "community_support": 8.0,
            "average": 8.7,
            "justification": "FastAPI's auto-documentation and Python ecosystem are ideal for a solo developer building a data-focused API. Async support handles concurrent dashboard requests well at this scale."
        },
        {
            "name": "Express.js",
            "requirements_fit": 7.5,
            "learning_curve": 7.5,
            "scalability": 8.0,
            "cost": 10.0,
            "community_support": 9.0,
            "average": 8.4,
            "justification": "Express is flexible and well-supported but requires more manual setup for validation and documentation that FastAPI provides automatically. Same-language benefit with a React frontend is notable."
        },
        {
            "name": "Django",
            "requirements_fit": 7.0,
            "learning_curve": 6.5,
            "scalability": 8.0,
            "cost": 10.0,
            "community_support": 8.5,
            "average": 8.0,
            "justification": "Django's batteries-included approach provides a lot for free but the framework is heavier than needed for a focused API. The admin panel is useful but the learning curve is steeper for someone used to lighter frameworks."
        }
    ],
    "database": [
        {
            "name": "Supabase (PostgreSQL)",
            "requirements_fit": 9.5,
            "learning_curve": 8.0,
            "scalability": 8.5,
            "cost": 9.5,
            "community_support": 8.0,
            "average": 8.7,
            "justification": "Supabase's free tier and built-in REST API dramatically reduce development time. PostgreSQL's analytical functions are perfectly suited for fitness metric aggregations and time-series queries."
        },
        {
            "name": "PlanetScale",
            "requirements_fit": 6.5,
            "learning_curve": 7.0,
            "scalability": 9.0,
            "cost": 7.5,
            "community_support": 7.0,
            "average": 7.4,
            "justification": "PlanetScale offers excellent scaling but MySQL's lack of window functions makes fitness data analytics queries more complex. Free tier row read limits could be restrictive for dashboard-heavy usage."
        },
        {
            "name": "Firebase Firestore",
            "requirements_fit": 6.0,
            "learning_curve": 7.5,
            "scalability": 8.0,
            "cost": 7.0,
            "community_support": 8.5,
            "average": 7.4,
            "justification": "Firestore's real-time sync is great for leaderboards but NoSQL makes time-range aggregation queries cumbersome. Read-heavy dashboard pages could exhaust the daily free tier limits quickly."
        }
    ],
    "hosting": [
        {
            "name": "Vercel",
            "requirements_fit": 8.5,
            "learning_curve": 9.0,
            "scalability": 8.0,
            "cost": 9.5,
            "community_support": 8.5,
            "average": 8.7,
            "justification": "Vercel's zero-config deployment and generous free tier eliminate DevOps overhead entirely for a solo developer. The 10-second function timeout is the only concern but is manageable at this scale."
        },
        {
            "name": "Railway",
            "requirements_fit": 7.5,
            "learning_curve": 8.0,
            "scalability": 8.0,
            "cost": 7.0,
            "community_support": 7.0,
            "average": 7.5,
            "justification": "Railway supports full-stack deployment but the 500-hour monthly limit on the free tier is restrictive for an always-on backend. Better suited as a secondary backend host alongside Vercel for frontend."
        },
        {
            "name": "Fly.io",
            "requirements_fit": 6.5,
            "learning_curve": 5.5,
            "scalability": 8.5,
            "cost": 8.0,
            "community_support": 6.5,
            "average": 7.0,
            "justification": "Fly.io's edge computing is powerful but requires Docker knowledge that conflicts with the beginner DevOps skill level. Setup complexity is not justified for a small-scale fitness dashboard."
        }
    ],
    "auth": [
        {
            "name": "Supabase Auth",
            "requirements_fit": 9.5,
            "learning_curve": 8.5,
            "scalability": 8.0,
            "cost": 10.0,
            "community_support": 7.5,
            "average": 8.7,
            "justification": "Using Supabase for both database and auth eliminates an entire integration layer. Row-level security policies simplify authorization logic significantly for a solo developer managing everything."
        },
        {
            "name": "Clerk",
            "requirements_fit": 7.5,
            "learning_curve": 8.0,
            "scalability": 8.0,
            "cost": 8.5,
            "community_support": 7.5,
            "average": 7.9,
            "justification": "Clerk's pre-built UI components save development time but add an external dependency. The 10K MAU free tier is generous enough but unnecessary if already using Supabase."
        },
        {
            "name": "Auth0",
            "requirements_fit": 5.5,
            "learning_curve": 6.0,
            "scalability": 9.0,
            "cost": 7.0,
            "community_support": 8.5,
            "average": 7.2,
            "justification": "Auth0 is enterprise-grade overkill for a small fitness dashboard. The complexity and branding restrictions on the free tier are not justified when simpler alternatives exist for this scale."
        }
    ]
}

MOCK_REPORT_RESPONSE = """# Tech Stack Recommendation Report

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
*Generated by Tech Stack Recommender — an agentic AI system*"""
