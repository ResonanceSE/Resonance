import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt({
  files: ['**/*.ts', '**/*.tsx','**/*.vue'],
  rules: {
    'no-console': 'off',
    'no-unused-vars': 'warn',
    '@typescript-eslint/no-unused-vars': 'warn' 
  },
})