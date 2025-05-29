import type { ReactNode } from 'react';
import "./ArabicSpeechExplanation.css"

interface ArabicSpeechExplanationProps {
  children: ReactNode;
  // You can add more props here if needed
}

function ArabicSpeechExplanation({children}: ArabicSpeechExplanationProps) {
    return (
        <div className="arabic-speech-explanation">
            {children}
        </div>
    );
}

export default ArabicSpeechExplanation;