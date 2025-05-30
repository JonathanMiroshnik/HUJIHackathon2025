import { useState, useEffect, useContext } from 'react'
import SpeechBubble from '../../components/SpeechBubble/SpeechBubble';
import ArabicSpeechBubble from '../../components/ArabicSpeechBubble/ArabicSpeechBubble';
import type { LanguageSpeech } from '../../components/SpeechBubble/SpeechBubble';
import Navigation from '../../components/Navigation/Navigation';
import './MainPage.css'
import TTSPlayer from '../../components/TTSPlayer/TTSPlayer';
import { useAppContext } from '../../contexts/AppContext';
import type { StudentState } from '../../contexts/AppContext';

function MainPage() {  
  const context = useAppContext(); 
  const [humanResponse, setHumanResponse] = useState<string>("");
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHumanResponse(e.target.value);
  };

  function arrayToLanguageSpeechArray(arr: any[]) {
    if (arr.length <= 0) {
      return [];
    }

    var retArr: LanguageSpeech[] = [];
    arr.map((ls) => {
      retArr.push({text: ls[0], language: ls[1]});
    })

    return retArr;
  }

  async function sendHumanMessage(message: string) {
    // try {
    //   const response = await fetch("http://localhost:8000/student", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify({ input: message }),
    //   });

    //   const result = await response.json();
    //   console.log(result);
    //   context.setStudent({
    //     name: result.name,
    //     age: result.age,
    //     gender: result.gender,
    //     background_info: result.background_info,
    //     arabic_proficiency_level: result.arabic_proficiency_level,
    //   });
    // } catch (err) {
    //   console.error("Error:", err);
    // }

    // const combined = Object.entries(context.student)
    // .map(([key, value]) => `${key}: ${value}`)
    // .join(', ');


     try {
        const response = await fetch("http://localhost:8000/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input: message }),
        });
        
        // combined + 

        const result = await response.json();
        context.addConversation(arrayToLanguageSpeechArray(result.message));
      } catch (err) {
        console.error("Error:", err);
      }
  }

  return (
      <div className="main-page">
        {/* <TTSPlayer /> */}
        <div className="conversation-container">
          {context.conversation.map((messages, index) => (
            <SpeechBubble key={"speech_bubble_text_"+index} subSpeeches={messages} speechBubbleIndex={index} />
          ))}
        </div>

        <footer className="footer-content">
          <button onClick={() => sendHumanMessage(humanResponse)} className="main-user-input-button"> לחץ כאן </button>
          <input onChange={handleChange} placeholder="לכתוב תגובה כאן" className="main-user-input"/>
        </footer>
      </div>
  )
}

export default MainPage;
