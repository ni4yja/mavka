import antfu from '@antfu/eslint-config'

export default antfu({
  ignores: ['**/*.js'],
  typescript: false,
  stylistic: {
    indent: 2,
    quotes: 'single',
  },
  rules: {
    'node/prefer-global/process': 'off',
    'node/prefer-global/buffer': 'off',
  },
})