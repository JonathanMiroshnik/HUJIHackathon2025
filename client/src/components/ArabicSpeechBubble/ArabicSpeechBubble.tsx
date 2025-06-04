import { useEffect, useState } from 'react';
import { BACKEND_URL } from '../../config/constants';
import ArabicSpeechExplanation from '../ArabicSpeechExplanation/ArabicSpeechExplanation';
import './ArabicSpeechBubble.css'

interface ArabicSpeechBubbleProps {
    text?: string;
    speechIndex?: number;
}

export interface WordExplanationProps {
    stem?: string;
    singular?: string;
    plural?: string;
    root?: string;
    meaning?: string;
    partOfSpeech?: string;
}

const WordExplanationPropsDict = {
    "stem": "בניין",
    "singular": "צורת יחיד",
    "plural": "צורת רבים",
    "root": "שורש",
    "meaning": "משמעות",
    "partOfSpeech": "חלק דיבר"
};


function ArabicSpeechBubble({text="", speechIndex=0}: ArabicSpeechBubbleProps) {
    const [explanation, setExplanation] = useState("");

    const [conversation, setConversation] = useState<string[]>([]);
    const [humanResponse, setHumanResponse] = useState("");

    const [highlighted, setHighlighted] = useState<[number, number] | null>(null);
    const [processing, setProcessing] = useState<boolean>(false);

    useEffect(() => {
        setConversation([text]);
    }, []);

    function iterateOverWordExplanationProps(props: WordExplanationProps): string {
        const ROW_SIZE = 2; // Must be above 0
        var retStr: string = "";
        var curCount: number = 0;

        for (const key in props) {
            if (props.hasOwnProperty(key)) {
                const typedKey = key as keyof WordExplanationProps;
                const value = props[typedKey];
                if (value === undefined || value === null) {
                    continue;
                }

                retStr += "| <b>" + WordExplanationPropsDict[typedKey] + "</b>: " + value + "\t     ";
                if (curCount % ROW_SIZE == 0) {
                    retStr += '\n';
                }
                curCount += 1;
            }
        }

        return retStr; // Make sure to return a string (or adjust the return type)
    }

    const sttSubmit = async (inText: string) => {
        const formData = new FormData();
        formData.append("text", inText);
    
        const response = await fetch(BACKEND_URL + "stt", {
          method: "POST",
          body: formData,
        });        
    
        if (!response.ok) {
          alert("Failed to fetch audio");
          return;
        }

        const reply = await response.json();
        const replyText: string[] = reply;
        highlightText([...replyText.map((word) => word.normalize("NFKC"))]);
    };

    // highlights the first conversation line with stt
    function highlightText(message: string[]) {
        const cleaned = conversation[0].replace(/,/g, '')
                                        .replace(/\./g, '')
                                        .replace(/،/g, '');
        const hlh = cleaned.split(' ');

        const highlightedHTML = hlh.map(word => {
                                    console.log("WORD", word, message.includes(word));
                                    return message.includes(word.normalize("NFKC"))
                                        ? word
                                        : `<b>${word}</b>`;
                                })
        .join(' ');
        
        console.log("convo", conversation);
        setConversation(prev => [highlightedHTML, ...prev.slice(1)])
    }

    const handleSubmit = async (inText: string) => {
        // const formData = new FormData();
        // formData.append("text", inText);
    
        // const response = await fetch(BACKEND_URL + "tts", {
        //   method: "POST",
        //   body: formData,
        // });
    
        // if (!response.ok) {
        //   alert("Failed to fetch audio");
        //   return;
        // }
    
        // const audioBlob = await response.blob();
        // const audioUrl = URL.createObjectURL(audioBlob);
    
        // const audio = new Audio(audioUrl);
        // audio.play();
    };    

    async function explanationClick(conversation: string[]) {
        setHighlighted(null);

        try {
            const response = await fetch(BACKEND_URL + `arabic-speech-explanation`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: conversation }),
            });

            const result = await response.json();
            console.log(result);
            setExplanation(result.data);
            console.log(conversation);
        } catch (err) {
            console.error("Error:", err);
        }
    }

    async function translateConversation(conversation: string[]) {
        setHighlighted(null);

        try {
            const response = await fetch(BACKEND_URL + `translate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: conversation }),
            });

            const result = await response.json();
            console.log(result);
            setExplanation(result.data);
            console.log(conversation);
        } catch (err) {
            console.error("Error:", err);
        }
    }

    async function continueConversationClick(conversation: string[]) {
        try {
            const response = await fetch(BACKEND_URL + `arabic-speech-continue-conversation`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: conversation }),
            });

            const result = await response.json();
            setConversation(prev => [...prev, result]);
            console.log(conversation);
        } catch (err) {
            console.error("Error:", err);
        }
    }

    async function handleWord(word: string, wordIndexes: [number, number]) {
        setHighlighted(wordIndexes);
        setProcessing(true);
        
        try {
            const response = await fetch(BACKEND_URL + `explain-word`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: word }),
            });

            const result = await response.json();
            if (!result || !result.data || !result.data.parts) {
                throw new Error("Word explanation did not properly return");
            }

            const parts = result.data.parts;
            const resultRemade: WordExplanationProps = {
                stem: parts.binyan,
                singular: parts.singular, 
                plural: parts.plural,
                root: parts.root,
                meaning: parts.meaning,
                partOfSpeech: parts.partOfSpeech
            };

            handleSubmit(word);            
            setExplanation(iterateOverWordExplanationProps(resultRemade));

            setProcessing(false);
        } catch (err) {
            setProcessing(false);
            console.error("Error:", err);
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setHumanResponse(e.target.value);
    };

    // async function handleSpeechClick(word: string, type: string) {
    //     try {
    //         const response = await fetch(BACKEND_URL + `${type}`, {
    //             method: "POST",
    //             headers: { "Content-Type": "application/json" },
    //             body: JSON.stringify({ input: word }),
    //         });

    //         const result = await response.json();

    //         const resultRemade: WordExplanationProps = {
    //             stem: result.binyan,
    //             singular: result.singular, 
    //             plural: result.plural,
    //             root: result.root,
    //             // partOfSpeech: string;
    //         };

    //         handleSubmit(word);

    //         setWordExplanation(true);
    //         setLineExplanation(false);

    //         setExplanation(wordExplanationToString(resultRemade));
    //         // setExplanation(JSON.stringify(result, null, 2)); // TODO: break up word parameters
    //         console.log(conversation);
    //     } catch (err) {
    //         console.error("Error:", err);
    //     }
    // }    

    return (
        <div className="arabic-speech-bubble">
            { conversation.map((conv, ind) => 
                <div>
                    {conv.split(' ').map((word, index) => (
                        <span
                            key={"arabic_bubble_" + speechIndex + "_subBubble_" + ind + "_word_" + index}
                            className={`word ${highlighted && highlighted[0] === ind && highlighted[1] === index ? 'active-word' : ''}`}
                            onClick={() => handleWord(word, [ind, index])}
                        >
                            <a style={{color: "white"}} dangerouslySetInnerHTML={{ __html: word + ' '}} />
                        </span> 
                    ))  }
                </div>
            ) }
            { explanation && <ArabicSpeechExplanation processing={processing}> <div dangerouslySetInnerHTML={{ __html: explanation }}/> </ArabicSpeechExplanation>}
            <div className="arabic-speech-button-section">   
                <button onClick={() => sttSubmit(conversation[0])} className="arabic-speech-button">🗣️</button>
                <button onClick={() => handleSubmit(conversation.join('\n'))} className="arabic-speech-button">📢</button>
                <button onClick={() => explanationClick(conversation)} className="arabic-speech-button">הסבר</button>
                <button onClick={() => translateConversation(conversation)} className="arabic-speech-button">תרגום</button>
                <button onClick={() => continueConversationClick(conversation)} className="arabic-speech-button">המשך</button>                
                <input onChange={handleChange} className="arabic-speech-question-input" placeholder={`שאל על ${conversation.length > 1 ? "השיחה": "המשפט"}`} />
                <button onClick={() => explanationClick([...conversation, humanResponse])}> שלח </button>
            </div>
        </div>
    );
}

export default ArabicSpeechBubble;
