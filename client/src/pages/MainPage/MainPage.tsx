import { useState, useEffect } from 'react'
import SpeechBubble from '../../components/SpeechBubble/SpeechBubble';
import ArabicSpeechBubble from '../../components/ArabicSpeechBubble/ArabicSpeechBubble';
import './MainPage.css'

function MainPage() {
  const [humanResponse, setHumanResponse] = useState<string>("");
  const [conversation, setConversation] = useState<string[]>([]);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHumanResponse(e.target.value);
  };

  async function sendHumanMessage(message: string) {
     try {
        const response = await fetch("http://localhost:8000/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input: message }),
        });

        const result = await response.json();
        setConversation(prev => [...prev, result.message]);
        console.log(conversation);
      } catch (err) {
        console.error("Error:", err);
      }
  }

  return (
      <div className="main-page">  
        <SpeechBubble />

        {conversation.map((message, index) => (
          // message={message}
          <ArabicSpeechBubble key={"arabic_text_"+index} text={message} />
        ))}

        <footer className="footer-content">
          <button onClick={() => sendHumanMessage(humanResponse)} className="main-user-input-button"> לחץ כאן </button>
          <input onChange={handleChange} placeholder="לכתוב תגובה כאן" className="main-user-input"/>
        </footer>
      </div>   
  )
}

export default MainPage;