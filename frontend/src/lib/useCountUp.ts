import { useEffect, useRef, useState } from 'react'

/**
 * Animates a number counting up to `target`, like a ticker readout
 * settling on a fresh quote. Respects prefers-reduced-motion by jumping
 * straight to the final value.
 */
export function useCountUp(target: number, duration = 700): number {
  const [value, setValue] = useState(target)
  const fromRef = useRef(0)
  const startRef = useRef<number | null>(null)

  useEffect(() => {
    const prefersReduced =
      typeof window !== 'undefined' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (prefersReduced) {
      setValue(target)
      return
    }

    fromRef.current = 0
    startRef.current = null
    let frame: number

    function step(timestamp: number) {
      if (startRef.current === null) startRef.current = timestamp
      const elapsed = timestamp - startRef.current
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(fromRef.current + (target - fromRef.current) * eased)
      if (progress < 1) frame = requestAnimationFrame(step)
    }

    frame = requestAnimationFrame(step)
    return () => cancelAnimationFrame(frame)
  }, [target, duration])

  return value
}
