# Go-Enhance ({YOUR_COMPANY} Solutions Landing Page)

## Project Overview

A React-based landing page for {YOUR_COMPANY} Solutions, featuring an interactive ROI calculator for custom AI-powered CRM solutions.

## Tech Stack

- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS + shadcn-ui (Radix UI)
- **Routing:** React Router DOM
- **State/Forms:** React Hook Form + Zod + TanStack Query
- **Charts:** Recharts

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app runs at **http://localhost:8080**

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Build for production |
| `npm run lint` | Run ESLint |
| `npm run preview` | Preview production build |

## Project Structure

```
src/
├── pages/           # Route pages (Index, NotFound)
├── components/      # UI components
│   ├── ui/          # shadcn-ui primitives (51 components)
│   ├── Header.tsx
│   ├── Hero.tsx
│   ├── ROICalculator.tsx
│   └── ...
├── hooks/           # Custom React hooks
├── lib/             # Utilities
├── App.tsx          # Main app with routing
└── main.tsx         # Entry point
```

## Path Aliases

Use `@/` to import from `src/`:
```typescript
import { Button } from "@/components/ui/button"
```

## Notes

- TypeScript configured with relaxed strict settings
- UI components from shadcn-ui are in `src/components/ui/`
