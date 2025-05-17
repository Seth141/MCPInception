# MCPInception Frontend

This is the frontend application for MCPInception, built with Next.js, TypeScript, and Tailwind CSS.

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Create a `.env.local` file in the frontend directory with the following variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Building for Production

```bash
npm run build
# or
yarn build
```

### Running Production Build

```bash
npm run start
# or
yarn start
```

## Project Structure

- `src/app/` - Next.js app directory containing pages and layouts
- `src/components/` - Reusable React components
- `src/lib/` - Utility functions and API clients
- `public/` - Static assets

## Technologies Used

- Next.js 14
- TypeScript
- Tailwind CSS
- React Query
- Axios
- Headless UI
- Heroicons
