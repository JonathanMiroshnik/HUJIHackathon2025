import HebrewSpeechBubble from '../HebrewSpeechBubble/HebrewSpeechBubble';
import ArabicSpeechBubble from '../ArabicSpeechBubble/ArabicSpeechBubble';
import './SpeechBubble.css'

export interface LanguageSpeech {
    text: string;
    language: string; // Appropriate strings: "Hebrew", "Arabic"
}

interface SpeechBubbleProps {
    subSpeeches: LanguageSpeech[];
    speechBubbleIndex: number;
}

function SpeechBubble({ subSpeeches, speechBubbleIndex }: SpeechBubbleProps) {
    return (
        <div className="speech-bubble">
            { subSpeeches.length > 0 && subSpeeches.map((ss, ind) => (
                <div key={"speech-bubble_" + speechBubbleIndex + "_sub-speech_" + ind}>                    
                    {ss.language === "Hebrew" ? 
                    <HebrewSpeechBubble>{ss.text}</HebrewSpeechBubble> : 
                    <ArabicSpeechBubble text={ss.text} speechIndex={ind} />}
                </div>
            )) }            
        </div>
    );
}

export default SpeechBubble;