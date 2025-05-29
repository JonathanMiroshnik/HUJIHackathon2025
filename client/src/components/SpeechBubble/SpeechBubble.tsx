import HebrewSpeechBubble from '../HebrewSpeechBubble/HebrewSpeechBubble';
import ArabicSpeechBubble from '../ArabicSpeechBubble/ArabicSpeechBubble';
import './SpeechBubble.css'

function SpeechBubble() {
    return (
        <div className="speech-bubble">
            <HebrewSpeechBubble>שלום קוראים לי איש</HebrewSpeechBubble>
            <ArabicSpeechBubble text="أحد أبرز الأحداث في التاريخ " />
        </div>
    );
}

export default SpeechBubble;