# Node.js / TypeScript Conventions

- Prefer TypeScript for new modules.
- Use ESLint + Prettier formatting defaults.
- Keep npm scripts explicit (`build`, `test`, `lint`, `dev`).
- Avoid runtime secrets in checked-in config files.

## Verification Commands

- **Test**: `npm test` or `npm run test`
- **Lint**: `npm run lint` or `eslint .`
- **Type check**: `tsc --noEmit` or `npm run typecheck`
- **Build**: `npm run build`
