FROM node:22-alpine

WORKDIR /workspace/apps/dashboard

COPY apps/dashboard/package.json /workspace/apps/dashboard/package.json
COPY apps/dashboard/tsconfig.json /workspace/apps/dashboard/tsconfig.json
COPY apps/dashboard/next.config.mjs /workspace/apps/dashboard/next.config.mjs
COPY apps/dashboard/next-env.d.ts /workspace/apps/dashboard/next-env.d.ts

RUN npm install

COPY apps/dashboard /workspace/apps/dashboard

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
