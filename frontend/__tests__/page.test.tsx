describe('FastCV AI Application', () => {
  it('should pass basic test', () => {
    expect(1 + 1).toBe(2)
  })

  it('should have environment variables available', () => {
    expect(typeof process.env.NODE_ENV).toBe('string')
  })
})
