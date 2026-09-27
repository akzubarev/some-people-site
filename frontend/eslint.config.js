import js from '@eslint/js'
import ts from 'typescript-eslint'
import hooks from 'eslint-plugin-react-hooks'
export default [
  { ignores: ['src/shared/api/schema.ts'] },
  js.configs.recommended,
  ...ts.configs.recommended,
  { files: ['**/*.{ts,tsx}'], plugins: { 'react-hooks': hooks },
    rules: { ...hooks.configs.recommended.rules } },
]
