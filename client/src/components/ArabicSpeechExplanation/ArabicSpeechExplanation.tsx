import type { ReactNode } from 'react';
import "./ArabicSpeechExplanation.css"

interface ArabicSpeechExplanationProps {
  children: ReactNode;
  processing?: boolean;
  // You can add more props here if needed
}

function ArabicSpeechExplanation({children, processing=false}: ArabicSpeechExplanationProps) {
    return (
        <div>
            <div className="arabic-speech-explanation">
                {children}
            </div>
            { processing && "⏳" }
        </div>
    );
}

export default ArabicSpeechExplanation;