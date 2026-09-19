// Invalidate responses that were started by a previous signed-in session.
let version = 0
export const sessionVersion = () => version
export const invalidateSession = () => { version += 1 }
