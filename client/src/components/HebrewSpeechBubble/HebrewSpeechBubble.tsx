import './HebrewSpeechBubble.css';
import type { ReactNode } from 'react';

interface HebrewSpeechBubbleProps {
  children: ReactNode;
  // You can add more props here if needed
}

function HebrewSpeechBubble({ children }: HebrewSpeechBubbleProps) {
  return (
    <div className="hebrew-speech-bubble">
      { children }
    </div>
  );
}

export default HebrewSpeechBubble;