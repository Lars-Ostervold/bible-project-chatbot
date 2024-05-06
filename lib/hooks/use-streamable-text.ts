import { StreamableValue, readStreamableValue } from 'ai/rsc'
import { useEffect, useState } from 'react'

export const useStreamableText = (
  content: string | StreamableValue<string>
) => {
  const [state, setState] = useState({
    text: typeof content === 'string' ? content : '',
    done: typeof content === 'string'
  });

  useEffect(() => {
    ;(async () => {
      if (typeof content === 'object') {
        let value = ''
        for await (const delta of readStreamableValue(content)) {
          if (typeof delta === 'string') {
            value = value + delta;
            setState({ text: value, done: false });
          }
        }
        setState(prevState => ({ ...prevState, done: true }));
      }
    })()
  }, [content])

  return state;
}
