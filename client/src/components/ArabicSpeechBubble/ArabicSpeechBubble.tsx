import { useEffect, useState } from 'react';
import ArabicSpeechExplanation from '../ArabicSpeechExplanation/ArabicSpeechExplanation';
import './ArabicSpeechBubble.css'

interface ArabicSpeechBubbleProps {
    text?: string;
    speechIndex?: number;
}

function ArabicSpeechBubble({text="", speechIndex=0}: ArabicSpeechBubbleProps) {
    const [explanation, setExplanation] = useState("");
    const [conversation, setConversation] = useState<string[]>([]);
    const [humanResponse, setHumanResponse] = useState("");

    async function explanationClick(conversation: string[]) {
        try {
            const response = await fetch(`http://localhost:8000/arabic-speech-explanation`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: conversation }),
            });

            const result = await response.json();
            setExplanation(result.message);
            console.log(conversation);
        } catch (err) {
            console.error("Error:", err);
        }
    }

    useEffect(() => {
        setConversation([text]);
    }, []);

    async function continueConversationClick(conversation: string[]) {
        try {
            const response = await fetch(`http://localhost:8000/arabic-speech-continue-conversation`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: conversation }),
            });

            const result = await response.json();
            setConversation(prev => [...prev, result.message]);
            console.log(conversation);
        } catch (err) {
            console.error("Error:", err);
        }
    }

    async function handleSpeechClick(word: string, type: string) {
        try {
            const response = await fetch(`http://localhost:8000/${type}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: word }),
            });

            const result = await response.json();
            setExplanation(JSON.stringify(result, null, 2)); // TODO: break up word parameters
            console.log(conversation);
        } catch (err) {
            console.error("Error:", err);
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setHumanResponse(e.target.value);
    };

    return (
        <div className="arabic-speech-bubble">
            { conversation.map((conv, ind) => 
                <div>
                    {conv.split(' ').map((word, index) => (
                        <span
                            key={"arabic_bubble_" + speechIndex + "_subBubble_" + ind + "_word_" + index}
                            // className={`word ${activeWord === word ? 'active' : ''}`} // TODO: active word indicator
                            onClick={() => handleSpeechClick(word, "explain-word")}
                        >
                            {word + ' '}
                        </span> 
                    ))  }
                </div>
             ) }
             { explanation && <ArabicSpeechExplanation> {explanation} </ArabicSpeechExplanation>}
            <div className="arabic-speech-button-section">
                <button onClick={() => explanationClick(conversation)} className="arabic-speech-button">הסבר</button>
                <button onClick={() => continueConversationClick(conversation)} className="arabic-speech-button">המשך</button>                
                <input onChange={handleChange} className="arabic-speech-question-input" placeholder={`שאל על ${conversation.length > 1 ? "השיחה": "המשפט"}`} />
                <button onClick={() => handleSpeechClick(humanResponse, "arabic-speech-explanation")}> שלח </button>
            </div>
        </div>
    );
}

export default ArabicSpeechBubble;
